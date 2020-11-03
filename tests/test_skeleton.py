# -*- coding: utf-8 -*-

import pytest
from jpack.skeleton import fib

__author__ = "Stefan Weissenberger"
__copyright__ = "Stefan Weissenberger"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
