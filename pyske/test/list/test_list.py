"""
Tests for additional functions on Python's lists.
"""

import operator
from pyske.core.support.list import scan


# -------------------------- #

def test_scan_nil():
    # pylint: disable=missing-docstring
    neutral = 0
    a_list = []
    res = scan(a_list, operator.add, neutral)
    exp = [0]
    assert res == exp


def test_scan_cons():
    # pylint: disable=missing-docstring
    neutral = 0
    a_list = [1, 2, 3, 4]
    res = scan(a_list, operator.add, neutral)
    exp = [0, 1, 3, 6, 10]
    assert res == exp
