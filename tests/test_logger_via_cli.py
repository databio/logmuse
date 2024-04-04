""" Tests for call to setup and get logger from CLI opts/args """

import argparse
import logging
import sys
from hypothesis import given, strategies as st
import pytest
from logmuse import add_logging_options, logger_via_cli
from logmuse.est import (
    AbsentOptionException,
    LEVEL_BY_VERBOSITY,
    LOGGING_CLI_OPTDATA,
    SILENCE_LOGS_OPTNAME,
    VERBOSITY_OPTNAME,
    _MIN_VERBOSITY,
    _MAX_VERBOSITY,
)


__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


VERBOSITY_OPTNAME = "--" + VERBOSITY_OPTNAME


@pytest.fixture
def parser():
    """Update empty argument parser with standard logging options."""
    return add_logging_options(argparse.ArgumentParser())


@pytest.mark.parametrize("missing", list(LOGGING_CLI_OPTDATA.keys()))
@pytest.mark.parametrize("strict", [False, True])
def test_opts_not_added(parser, missing, strict):
    """Special exception occurs when it appears that log opts are absent."""
    opts = parser.parse_args([])
    assert all(hasattr(opts, _rawopt(n)) for n in LOGGING_CLI_OPTDATA)
    delattr(opts, _rawopt(missing))
    assert not hasattr(opts, _rawopt(missing))

    def create_logger():
        return logger_via_cli(opts, strict=strict)

    if strict:
        with pytest.raises(AbsentOptionException):
            create_logger()
    else:
        assert isinstance(create_logger(), logging.Logger)


def test_repeat_parser_configuration_is_exceptional(parser):
    """add_logging_options must be called just once."""
    with pytest.raises(argparse.ArgumentError):
        add_logging_options(parser)  # Parser already has the logging options.


def test_opts_added_none_used(parser):
    """Addition of logging options allows logger_via_cli to complete."""
    opts = parser.parse_args([])
    assert all(hasattr(opts, _rawopt(n)) for n in LOGGING_CLI_OPTDATA)
    logger = logger_via_cli(opts)
    assert isinstance(logger, logging.Logger)


@pytest.mark.parametrize(
    ["cmdl", "flag", "hdlr_type"],
    [
        (["--" + SILENCE_LOGS_OPTNAME], True, logging.NullHandler),
        ([], False, logging.StreamHandler),
    ],
)
def test_silence(parser, cmdl, flag, hdlr_type):
    """Log silencing generates a null handler."""
    opts = parser.parse_args(cmdl)
    assert getattr(opts, SILENCE_LOGS_OPTNAME.lstrip("-")) is flag
    logger = logger_via_cli(opts)
    hs = logger.handlers
    assert 1 == len(hs)
    assert isinstance(hs[0], hdlr_type)


@pytest.mark.parametrize("verbosity", range(_MIN_VERBOSITY, _MAX_VERBOSITY + 1))
def test_typical_verbosity(parser, verbosity):
    """Typical verbosity specifications yield logger with expected level."""
    opts = parser.parse_args([VERBOSITY_OPTNAME, str(verbosity)])
    logger = logger_via_cli(opts)
    exp = getattr(logging, LEVEL_BY_VERBOSITY[verbosity - 1])
    _assert_level(logger, exp)


@given(verbosity=st.integers(-sys.maxsize, -1))
def test_negative_verbosity(parser, verbosity):
    """Verbosity is pulled up to min logging level."""
    with pytest.raises(SystemExit):
        parser.parse_args([VERBOSITY_OPTNAME, str(verbosity)])


@given(verbosity=st.integers(len(LEVEL_BY_VERBOSITY) + 1, sys.maxsize))
def test_excess_verbosity(parser, verbosity):
    """Verbosity saturates / maxes out."""
    with pytest.raises(SystemExit):
        parser.parse_args([VERBOSITY_OPTNAME, str(verbosity)])


@pytest.mark.parametrize("verbosity", ["a", "NOTALEVEL", 2.5])
def test_invalid_verbosity_is_exceptional(parser, verbosity):
    """Verbosity must be a valid level name or an integer."""
    with pytest.raises(SystemExit):
        parser.parse_args([VERBOSITY_OPTNAME, str(verbosity)])


def _assert_level(log, lev):
    """
    Assert expectation on level of logger and all its handlers.

    :param logging.Logger log: logger instance to test
    :param int lev: expected level of logger and its handlers
    """
    assert lev == log.level
    assert all(lev == h.level for h in log.handlers)


def _rawopt(n):
    """Reduce option name."""
    return n.lstrip("--").lstrip("-")
