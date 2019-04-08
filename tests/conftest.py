""" Test fixture setup and general functional sharing """

import argparse
import pytest

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.fixture
def parser():
    """ Clean/fresh, blank-slate argument parser instance for a test case """
    return argparse.ArgumentParser()
