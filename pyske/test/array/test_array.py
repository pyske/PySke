"""
Tests for PySke Sequential Array
"""

__all__ = []

from operator import add, mul

import pytest

from pyske.core.array.sarray import SArray
from pyske.core.util import fun

pytestmark = pytest.mark.sarray  # pylint: disable=invalid-name


def first(value, _):
    """Return its first argument"""
    return value


def pair(fst, snd):
    """Build a pair"""
    return fst, snd


# -------------------------- #

def test_length_empty():
    # pylint: disable=missing-docstring
    arr = SArray('f')
    exp = 0
    res = arr.length()
    assert res == exp


def test_length_non_empty():
    # pylint: disable=missing-docstring
    size = 11
    arr = SArray('i', range(0, size))
    exp = size
    res = arr.length()
    assert res == exp


# -------------------------- #

def test_init_empty():
    # pylint: disable=missing-docstring
    res = SArray.init(fun.idt, 0)
    exp = SArray('i')
    assert res == exp


def test_init_non_empty():
    # pylint: disable=missing-docstring
    size = 11
    res = SArray.init(fun.incr, size)
    exp = SArray('i', range(1, size + 1))
    assert res == exp


# -------------------------- #

def test_map_empty():
    # pylint: disable=missing-docstring
    arr = SArray('d')
    exp = SArray('d')
    res = arr.map(fun.idt)
    assert res == exp


def test_map_incr():
    # pylint: disable=missing-docstring
    arr = SArray('i', [1, 2, 3])
    exp = SArray('i', [2, 3, 4])
    res = arr.map(fun.incr)
    assert res == exp


def test_map_id():
    # pylint: disable=missing-docstring
    arr = SArray('f', [1, 2, 3])
    exp = SArray('f', [1, 2, 3])
    res = arr.map(fun.idt)
    assert res == exp


# -------------------------- #

def test_mapi_empty():
    # pylint: disable=missing-docstring
    arr = SArray('i')
    exp = SArray('i')
    res = arr.mapi(pair)
    assert res == exp


def test_mapi_non_empty():
    # pylint: disable=missing-docstring
    arr = SArray('i', [1, 2, 3])
    exp = SArray('f', [0, 2, 6])
    res = arr.mapi(mul)
    assert res == exp


def test_mapi_id():
    # pylint: disable=missing-docstring
    exp = SArray('i', [0, 1, 2])
    arr = SArray('f', [1, 2, 3])
    res = arr.mapi(first)
    assert res == exp


# -------------------------- #

def test_map2_empty():
    # pylint: disable=missing-docstring
    data = SArray('i')
    exp = SArray('i')
    res = data.map2(add, data)
    assert res == exp


def test_map2_non_empty():
    # pylint: disable=missing-docstring
    data = SArray('i', [1, 2, 3])
    exp = SArray('i', [2, 4, 6])
    res = data.map2(add, data)
    assert res == exp


# -------------------------- #

def test_reduce_empty():
    # pylint: disable=missing-docstring
    data = SArray('f')
    initial = 42.0
    res = data.reduce(add, initial)
    exp = initial
    assert res == exp


def test_reduce_non_empty():
    # pylint: disable=missing-docstring
    size = 111
    data = SArray.init(fun.idt, size)
    res = data.reduce(add)
    exp = int(((size - 1) * size) / 2)
    assert res == exp


# -------------------------- #

def test_scan_empty():
    # pylint: disable=missing-docstring
    data = SArray('f')
    initial = 42.0
    res = data.scan(add, initial)
    exp = SArray('f', [initial])
    assert res == exp


def test_scan_non_empty():
    # pylint: disable=missing-docstring
    size = 111
    data = SArray.init(lambda x: 1, size)
    res = data.scan(add, 0)
    exp = SArray.init(fun.idt, size + 1)
    assert res == exp


# -------------------------- #

def test_scanl_empty():
    # pylint: disable=missing-docstring
    data = SArray('f')
    initial = 42.0
    res = data.scanl(add, initial)
    exp = data
    assert res == exp


def test_scanl_non_empty():
    # pylint: disable=missing-docstring
    size = 111
    data = SArray.init(lambda x: 1, size)
    res = data.scanl(add, 0)
    exp = SArray.init(fun.idt, size)
    assert res == exp


# -------------------------- #

def test_scanl_last_empty():
    # pylint: disable=missing-docstring
    data = SArray('f')
    initial = 42.0
    res = data.scanl_last(add, initial)
    exp = (data, initial)
    assert res == exp


def test_scanl_last_non_empty():
    # pylint: disable=missing-docstring
    size = 111
    data = SArray.init(lambda x: 1, size)
    res = data.scanl_last(add, 0)
    exp = (SArray.init(fun.idt, size), 111)
    assert res == exp


# -------------------------- #

def test_filter_empty():
    # pylint: disable=missing-docstring
    data = SArray('f')
    res = data.filter(lambda x: x == 0.0)
    exp = data
    assert res == exp


def test_filter_non_empty():
    # pylint: disable=missing-docstring
    size = 111
    data = SArray.init(float, size)
    res = data.filter(lambda x: x != 0.0)
    exp = SArray.init(lambda x: float(x + 1), size - 1)
    assert res == exp
