"""
Tests of sequential lists
"""

import operator
import pytest
from pyske.core.util import fun
from pyske.core.list.slist import SList


def parser_tuple(string):
    """
    Returns a pair of string from a string of comma separate elements.

    :param string: str
    :return: pair
    """
    string = string.replace("(", "")
    string = string.replace(")", "")
    strings = string.split(",")
    return int(strings[0]), int(strings[1])

# -------------------------- #


def test_head_empty():
    # pylint: disable=missing-docstring
    slst = SList()
    exp = None
    res = slst.head()
    assert res == exp


def test_head_one():
    # pylint: disable=missing-docstring
    slst = SList()
    exp = 1
    slst.append(exp)
    res = slst.head()
    assert res == exp


def test_head_several():
    # pylint: disable=missing-docstring
    slst = SList()
    exp = 1
    slst.append(exp)
    slst.append(exp + 1)
    res = slst.head()
    assert res == exp


# -------------------------- #

def test_tail_empty():
    # pylint: disable=missing-docstring
    slst = SList()
    exp = SList()
    res = slst.tail()
    assert res == exp


def test_tail_one():
    # pylint: disable=missing-docstring
    slst = SList([1])
    exp = SList()
    res = slst.tail()
    assert res == exp


def test_tail_several():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3])
    exp = SList([2, 3])
    res = slst.tail()
    assert res == exp


# -------------------------- #

def test_length_nil():
    # pylint: disable=missing-docstring
    slst = SList()
    exp = 0
    res = slst.length()
    assert res == exp


def test_length_cons():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3])
    exp = 3
    res = slst.length()
    assert res == exp


# -------------------------- #

def test_filter():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3, 4, 5, 6, 7, 8])
    res = slst.filter(lambda val: val % 2 == 0)
    for value in res:
        assert value % 2 == 0


# -------------------------- #

def test_empty_true():
    # pylint: disable=missing-docstring
    slst = SList()
    exp = True
    res = slst.empty()
    assert res == exp


def test_empty_false():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3])
    exp = False
    res = slst.empty()
    assert res == exp


# -------------------------- #

def test_map_empty():
    # pylint: disable=missing-docstring
    slst = SList()
    exp = SList()
    res = slst.map(fun.idt)
    assert res == exp


def test_map_inc():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3])
    exp = SList([2, 3, 4])
    res = slst.map(fun.incr)
    assert res == exp


def test_map_id():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3])
    exp = SList([1, 2, 3])
    res = slst.map(fun.idt)
    assert res == exp


# -------------------------- #

def test_mapi_empty():
    # pylint: disable=missing-docstring
    slst = SList()
    exp = SList()
    res = slst.mapi(lambda i, val: (i, val))
    assert res == exp


def test_mapi_non_empty():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3])
    exp = SList([0, 2, 6])
    res = slst.mapi(operator.mul)
    assert res == exp


def test_mapi_id():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3])
    exp = SList([1, 2, 3])
    res = slst.mapi(lambda i, val: val)
    assert res == exp


# -------------------------- #

def test_map_reduce_nil():
    # pylint: disable=missing-docstring
    initial = 1232
    slst = SList()
    res = slst.map_reduce(fun.incr, operator.add, initial)
    exp = initial
    assert res == exp


def test_map_reduce_cons():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3, 4])
    res = slst.map_reduce(fun.incr, operator.add)
    exp = slst.map(fun.incr).reduce(operator.add)
    assert res == exp


# -------------------------- #


def test_reduce_nil():
    # pylint: disable=missing-docstring
    initial = 1232
    slst = SList()
    res = slst.reduce(operator.add, initial)
    exp = initial
    assert res == exp


def test_reduce_cons():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3, 4])
    res = slst.reduce(operator.add)
    exp = 10
    assert res == exp


def test_reduce_sum_empty():
    # pylint: disable=missing-docstring
    slst = SList()
    exp = 0
    res = slst.reduce(operator.add, 0)
    assert res == exp


def test_reduce_sum_non_empty():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3, 4, 5, 6])
    exp = 22
    res = slst.reduce(operator.add, 1)
    assert res == exp


# -------------------------- #

def test_scan_nil():
    # pylint: disable=missing-docstring
    neutral = 0
    slst = SList()
    res = slst.scan(operator.add, neutral)
    exp = SList([0])
    assert res == exp


def test_scan_cons():
    # pylint: disable=missing-docstring
    neutral = 0
    slst = SList([1, 2, 3, 4])
    res = slst.scan(operator.add, neutral)
    exp = SList([0, 1, 3, 6, 10])
    assert res == exp


# -------------------------- #

def test_scanr_empty():
    # pylint: disable=missing-docstring
    with pytest.raises(AssertionError):
        slst = SList()
        slst.scanr(operator.add)


def test_scanr_singleton():
    # pylint: disable=missing-docstring
    slst = SList([1])
    res = slst.scanr(operator.add)
    assert res == slst


def test_scanr_non_singleton():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3, 4])
    res = slst.scanr(operator.add)
    exp = SList([1, 3, 6, 10])
    assert res == exp


def fct(val1, val2):
    # pylint: disable=missing-docstring
    (num, num1) = val1
    (_, num2) = val2
    return num + num1, num2


def test_scanr_full_distribution():
    # pylint: disable=missing-docstring
    slst = SList([(0, 1), (1, 3), (0, 3), (0, 3), (0, 3)])
    res = slst.scanr(fct)
    exp = SList([(0, 1), (1, 3), (4, 3), (7, 3), (10, 3)])
    assert res == exp


def test_scanr_full_distribution2():
    # pylint: disable=missing-docstring
    slst = SList([(0, 1), (1, 3), (4, 3)])
    res = slst.scanr(fct)
    exp = SList([(0, 1), (1, 3), (4, 3)])
    assert res == exp


# -------------------------- #

def test_scanl_empty():
    # pylint: disable=missing-docstring
    slst = SList([])
    res = slst.scanl(operator.add, 0)
    exp = SList([])
    assert res == exp


def test_scanl_non_empty():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3, 4])
    res = slst.scanl(operator.add, 0)
    exp = SList([0, 1, 3, 6])
    assert res == exp


# -------------------------- #

def test_scanl_last_empty():
    # pylint: disable=missing-docstring
    slst = SList([])
    res = slst.scanl_last(operator.add, 0)
    exp = ([], 0)
    assert res == exp


def test_scanl_last_non_empty():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3, 4])
    res = slst.scanl_last(operator.add, 0)
    exp = (SList([0, 1, 3, 6]), 10)
    assert res == exp


# -------------------------- #

def test_scanp_nil():
    # pylint: disable=missing-docstring
    neutral = 0
    slst = SList()
    res = slst.scanp(operator.add, neutral)
    exp = SList([])
    assert res == exp


def test_scanp_cons():
    # pylint: disable=missing-docstring
    neutral = 0
    slst = SList([1, 2, 3, 4])
    res = slst.scanp(operator.add, neutral)
    exp = SList([9, 7, 4, 0])
    assert res == exp


# -------------------------- #

def test_zip_nil():
    # pylint: disable=missing-docstring
    sl1 = SList()
    sl2 = SList()
    res = sl1.zip(sl2)
    exp = SList()
    assert res == exp


def test_zip_cons():
    # pylint: disable=missing-docstring
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3, 4])
    res = sl1.zip(sl2)
    exp = SList([(1, 2), (2, 3), (3, 4)])
    assert res == exp


def test_zip_one_gt():
    # pylint: disable=missing-docstring
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3])
    with pytest.raises(AssertionError):
        sl1.zip(sl2)


def test_zip_one_lt():
    # pylint: disable=missing-docstring
    sl1 = SList([2, 3])
    sl2 = SList([2, 3, 4])
    with pytest.raises(AssertionError):
        sl1.zip(sl2)


# -------------------------- #

def test_zipwith_nil():
    # pylint: disable=missing-docstring
    sl1 = SList()
    sl2 = SList()
    res = sl1.map2(operator.add, sl2)
    exp = SList()
    assert res == exp


def test_zipwith_cons():
    # pylint: disable=missing-docstring
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3, 4])
    res = sl1.map2(operator.add, sl2)
    exp = SList([3, 5, 7])
    assert res == exp


def test_zipwith_one_gt():
    # pylint: disable=missing-docstring
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3])
    with pytest.raises(AssertionError):
        sl1.map2(operator.add, sl2)


def test_zipwith_one_lt():
    # pylint: disable=missing-docstring
    sl1 = SList([2, 3])
    sl2 = SList([2, 3, 4])
    with pytest.raises(AssertionError):
        sl1.map2(operator.add, sl2)


# -------------------------- #

def test_from_str_simple():
    # pylint: disable=missing-docstring
    string = "[1;2;3]"
    res = SList.from_str(string)
    exp = SList([1, 2, 3])
    assert res == exp


def test_from_str_tuple():
    # pylint: disable=missing-docstring
    string = "[(1,2);(3,4)]"
    res = SList.from_str(string, parser=parser_tuple)
    exp = SList([(1, 2), (3, 4)])
    assert res == exp

# -------------------------- #
