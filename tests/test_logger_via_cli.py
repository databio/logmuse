""" Tests for call to setup and get logger from CLI opts/args """

import argparse
import pytest
from logmuse import add_logging_options, logger_via_cli
from logmuse.est import AbsentOptionException, LOGGING_CLI_OPTDATA

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.fixture
def parser():
    """ Update empty argument parser with standard logging options. """
    return add_logging_options(argparse.ArgumentParser())


@pytest.mark.parametrize("missing", list(LOGGING_CLI_OPTDATA.keys()))
def test_opts_not_added(parser, missing):
    """ Special exception occurs when it appears that log opts are absent. """
    opts = parser.parse_args([])
    assert all(hasattr(opts, _rawopt(n)) for n in LOGGING_CLI_OPTDATA)
    delattr(opts, _rawopt(missing))
    assert not hasattr(opts, _rawopt(missing))
    with pytest.raises(AbsentOptionException):
        logger_via_cli(opts)


def _rawopt(n):
    """ Reduce option name. """
    return n.lstrip("--").lstrip("-")
