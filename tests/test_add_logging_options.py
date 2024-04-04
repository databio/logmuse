""" Tests for addition of logging options to CLI opt/arg parser """

import argparse
import random
import string
from logmuse import add_logging_options
from logmuse.est import LOGGING_CLI_OPTDATA
import pytest

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def pytest_generate_tests(metafunc):
    """Generation and parameterization of tests in this module."""
    if "opt" in metafunc.fixturenames:
        metafunc.parametrize(
            "opt", list(["--" + x for x in LOGGING_CLI_OPTDATA.keys()])
        )


def test_all_options_are_added(parser, opt):
    """If requested, all of the standard logging options are added."""
    assert opt not in _get_optnames(parser)
    add_logging_options(parser)
    assert opt in _get_optnames(parser)


def test_each_option_gis_functional(parser, opt):
    """Each added CLI opt can be used as expected."""
    add_logging_options(parser)
    for a in parser._actions:
        if opt in a.option_strings:
            use = get_act_use(parser, a)
            break
    else:
        pytest.fail(
            "Parser lacks action with name: {}; available: {}".format(
                opt, _get_optnames(parser)
            )
        )
    try:
        parser.parse_args(use)
    except Exception as e:
        pytest.fail("Use of option '{}' ({}) failed: {}".format(opt, use, e))


def get_act_use(p, act):
    """
    Create the pair of option name and argument to test usage in parser.

    :param argparse.ArgumentParser p: the parser instance with which to conduct
        the test
    :param argparse._StoreAction act: CLI action instance for which usage value(s)
        are to be generated
    :return list[str]: collection of command chunks that constitute usage of
        the given parser action
    """
    assert all(n in _get_optnames(p) for n in act.option_strings)
    return _build_action_usage(type(act))(act)


def _build_action_usage(act_kind):
    """
    Determine function to create command chunks needed to test action.

    :param type act_kind: the type of option action (e.g. StoreTrueAction)
    :return function(argparse._StoreAction) -> list[str]: function that when
        given a CLI action will create the representative command line chunks
    """
    from logmuse.est import _VERBOSITY_CHOICES, VERBOSITY_OPTNAME

    def get_general_use(act):
        name = _get_opt_first_name(act)
        arg = (
            random.choice(_VERBOSITY_CHOICES)
            if name == "--" + VERBOSITY_OPTNAME
            else _random_chars_option()
        )
        return [name, arg]

    strategies = [
        (
            (argparse._StoreTrueAction, argparse._StoreFalseAction),
            lambda a: [a.option_strings[0]],
        ),
        ((argparse._StoreAction), get_general_use),
    ]
    for kinds, strat in strategies:
        if issubclass(act_kind, kinds):
            return strat
    raise ValueError(
        "No usage strategies for given kind of option: {}".format(act_kind)
    )


def _get_optnames(p):
    """
    Get universe of option names known by given parser.

    :param argparse.ArgumentParser p: the parser instance to inspect
    :return Iterable[str]: full collection of option names known by the given
        parser, i.e. the entire space of CLI optname that may be used with it
    """
    return [n for a in p._actions for n in a.option_strings]


def _random_chars_option():
    """Randomly generate arbitrary text value for use as CLI opt argument."""
    pool = string.ascii_letters + string.digits
    return "".join(random.choice(pool) for _ in range(10))


def _get_opt_first_name(a):
    """Get the first of an action's option names."""
    return a.option_strings[0]
