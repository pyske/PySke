from pyske.core.support.errors import NotEqualSizeError, EmptyError
from pyske.core.array.sarray import SArray
import pytest


# -------------------------- #

def test_head_empty():
    sl = SArray('i')
    exp = None
    res = sl.head()
    assert res == exp


def test_head_one():
    sl = SArray('d')
    exp = 1
    sl.append(exp)
    res = sl.head()
    assert res == exp


def test_head_several():
    sl = SArray('i')
    exp = 1
    sl.append(exp)
    sl.append(exp + 1)
    res = sl.head()
    assert res == exp


# -------------------------- #

def test_tail_empty():
    sl = SArray('i')
    exp = SArray('i')
    res = sl.tail()
    assert res == exp


def test_tail_one():
    sl = SArray('d', [1])
    exp = SArray('d')
    res = sl.tail()
    assert res == exp


def test_tail_several():
    sl = SArray('d', [1, 2, 3])
    exp = SArray('d', [2, 3])
    res = sl.tail()
    assert res == exp


# -------------------------- #

def test_length_nil():
    sl = SArray('d')
    exp = 0
    res = sl.length()
    assert res == exp


def test_length_cons():
    sl = SArray('i', [1, 2, 3])
    exp = 3
    res = sl.length()
    assert res == exp


# -------------------------- #

def test_map_empty():
    sl = SArray('d')
    exp = SArray('d')
    f = lambda x: x
    res = sl.map(f)
    assert res == exp


def test_map_inc():
    sl = SArray('i', [1, 2, 3])
    exp = SArray('i', [2, 3, 4])
    f = lambda x: x + 1
    res = sl.map(f)
    assert res == exp


def test_map_id():
    sl = SArray('f', [1, 2, 3])
    exp = SArray('f', [1, 2, 3])
    f = lambda x: x
    res = sl.map(f)
    assert res == exp

# -------------------------- #

def test_mapi_empty():
    sl = SArray('i')
    exp = SArray('i')
    f = lambda i, x: (i, x)
    res = sl.mapi(f)
    assert res == exp


def test_mapi_non_empty():
    sl = SArray('i', [1, 2, 3])
    exp = SArray('f', [0, 2, 6])
    f = lambda i, x: i * x
    res = sl.mapi(f)
    assert res == exp


def test_mapi_id():
    sl = SArray('d', [1, 2, 3])
    exp = SArray('f', [1, 2, 3])
    f = lambda i, x: x
    res = sl.mapi(f)
    assert res == exp
