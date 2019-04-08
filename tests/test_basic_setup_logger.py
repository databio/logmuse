""" Tests for basic logger setup call """

import itertools
import logging
import sys
import pytest
from logmuse import setup_logger
from logmuse.est import DEFAULT_STREAM, LOGGING_LEVEL, PACKAGE_NAME

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.mark.parametrize(
    ["attr", "check"],
    [("level", (getattr(logging, LOGGING_LEVEL) if
                isinstance(LOGGING_LEVEL, str) else LOGGING_LEVEL,
                "Wrong logging level; expected {} but got {}")),
     ("name", (PACKAGE_NAME, "Wrong logger name; expected {} but got {}")),
     ("handlers", (1, "Wrong number of handlers; expected {} but got {}", len)),
     ("handlers", lambda h: _check_handler(h, loc=DEFAULT_STREAM))])
def test_all_defaults(attr, check):
    """ Check the values on the logger that result from all default arguments. """
    logger = setup_logger()
    if hasattr(check, "__call__"):
        fails = list(itertools.chain(*[check(obj) for obj in getattr(logger, attr)]))
        if fails:
            pytest.fail("Failures:\n{}".format("\n".join(fails)))
    else:
        try:
            exp, err_fmt = check
        except ValueError:
            exp, err_fmt, transform = check
        else:
            transform = None
        obs = getattr(logger, attr)
        obs = transform(obs) if transform else obs
        assert exp == obs, err_fmt.format(exp, obs)


@pytest.mark.parametrize(
    ["att", "val"],
    [("name", n) for n in ["arbitrary", "random"]] +
    [("level", x) for x in range(0, 50, 10)])
def test_single_attr(att, val):
    """ Test successful setting of a simple, particular logger attribute. """
    assert val == getattr(setup_logger(**{att: val}), att)


def test_make_non_root_name_root():
    """ Non-root name for root logger is prohibited. """
    with pytest.raises(ValueError):
        setup_logger("root", make_root=False)


@pytest.mark.parametrize(["make_root", "exp"],
    [(None, PACKAGE_NAME), (False, PACKAGE_NAME), (True, "root")])
def test_make_root(make_root, exp):
    """ Root status for logger has a couple of implications. """
    log = setup_logger(make_root=make_root)
    assert exp == log.name
    assert log.propagate is False


@pytest.mark.parametrize(
    ["kwargs", "exp"],
    [({}, False), ({"make_root": False}, False), ({"propagate": False}, False),
     ({"propagate": True}, True), ({"make_root": True}, False),
     ({"make_root": False, "propagate": False}, False),
     ({"make_root": False, "propagate": True}, True),
     ({"make_root": True, "propagate": False}, False),
     ({"make_root": True, "propagate": True}, True)])
def test_propagate(kwargs, exp):
    """ Determination of propagation flag considers root status and propagation. """
    assert setup_logger(**kwargs).propagate is exp


@pytest.mark.skip("not implemented")
def test_stream():
    """ Validate stream handler setting for created logger. """
    pass


@pytest.mark.skip("not implemented")
def test_logfile():
    """ Validate file handler setting for created logger. """
    pass


@pytest.mark.skip("not implemented")
def test_logfile_and_stream():
    """ Logging can be both stream and file. """
    pass


def _check_handler(h, lev=None, loc=None):
    """
    Check properties of a logging handler.

    :param logging.StreamHandler | logging.FileHandler h: handler to inspect
    :param str | int lev: expected handler level
    :param str | file loc: log output destination
    :return list[str]: any failure messages
    """
    fails = []
    if lev is not None:
        if isinstance(lev, str):
            lev = getattr(logging, lev)
        elif not isinstance(lev, int):
            raise TypeError("Expected logging level is neither string nor int: "
                            "{} ({})".format(lev, type(lev)))
        if h.level != lev:
            fails.append(
                "Wrong level (expected {} but got {})".format(lev, h.level))
    if loc is not None:
        if loc in [sys.stderr, sys.stdout]:
            exp_type = logging.StreamHandler
            obs_loc = h.stream
            exp_name = loc.name
            obs_name = h.stream.name
            if not isinstance(h, logging.StreamHandler):
                fails.append("Expected a stream handler but found {}".
                             format(type(h)))
            elif h.stream != loc:
                fails.append("Unexpected handler location; expected {} but "
                             "found {}".format(loc.name, h.stream.name))
        elif isinstance(loc, str):
            exp_type = logging.FileHandler
            obs_loc = h.stream.name
            exp_name = loc
            obs_name = h.stream.name
        else:
            raise TypeError(
                "Handler location to check is neither standard stream nor "
                "filepath: {} ({})".format(loc, type(loc)))
        if not isinstance(h, exp_type):
            fails.append("Expected a file handler but found {}".format(type(h)))
        if loc != obs_loc:
            fails.append("Unexpected handler location; expected {} but found {}".
                         format(exp_name, obs_name))
    return fails
