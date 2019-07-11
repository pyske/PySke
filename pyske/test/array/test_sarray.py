from pyske.core.array.sarray import SArray
from operator import add
import pytest
pytestmark = pytest.mark.sarray

def id(x):
    return x

def incr(x):
    return x + 1

# -------------------------- #

def test_length_empty():
    sl = SArray('f')
    exp = 0
    res = sl.length()
    assert res == exp


def test_length_non_empty():
    size = 11
    sl = SArray('i', range(0,size))
    exp = size
    res = sl.length()
    assert res == exp

# -------------------------- #

def test_init_empty():
    res = SArray.init(id, 0)
    exp = SArray('i')
    assert res == exp


def test_init_non_empty():
    size = 11
    res = SArray.init(incr, size)
    exp = SArray('i', range(1, size+1))
    assert res == exp

# -------------------------- #

def test_is_empty_empty():
    res = SArray.init(id, 0).is_empty()
    assert res


def test_is_empty_non_empty():
    size = 11
    res = SArray.init(incr, size).is_empty()
    assert not res

# -------------------------- #

def test_map_empty():
    sl = SArray('d')
    exp = SArray('d')
    res = sl.map(id)
    assert res == exp


def test_map_incr():
    sl = SArray('i', [1, 2, 3])
    exp = SArray('i', [2, 3, 4])
    res = sl.map(incr)
    assert res == exp


def test_map_id():
    sl = SArray('f', [1, 2, 3])
    exp = SArray('f', [1, 2, 3])
    res = sl.map(id)
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

# -------------------------- #

def test_map2_empty():
    input = SArray('i')
    exp = SArray('i')
    res = input.map2(add, input)
    assert res == exp


def test_map2_non_empty():
    input = SArray('i', [1, 2, 3])
    exp = SArray('i', [2, 4, 6])
    res = input.map2(add, input)
    assert res == exp

# -------------------------- #

def test_reduce_empty():
    input = SArray('f')
    c = 42.0
    res = input.reduce(add, c)
    exp = c
    assert res == exp

def test_reduce_non_empty():
    size = 111
    input = SArray.init(id, size)
    res = input.reduce(add)
    exp = int(((size-1)*size ) / 2)
    assert res == exp

# -------------------------- #

def test_scan_empty():
    input = SArray('f')
    c = 42.0
    res = input.scan(add, c)
    exp = SArray('f', [c])
    assert res == exp

def test_scan_non_empty():
    size = 111
    input = SArray.init(lambda x: 1, size)
    res = input.scan(add, 0)
    exp = SArray.init(id, size+1)
    assert res == exp

# -------------------------- #

def test_scanl_empty():
    input = SArray('f')
    c = 42.0
    res = input.scanl(add, c)
    exp = input
    assert res == exp

def test_scanl_non_empty():
    size = 111
    input = SArray.init(lambda x: 1, size)
    res = input.scanl(add, 0)
    exp = SArray.init(id, size)
    assert res == exp

# -------------------------- #

def test_scanl_last_empty():
    input = SArray('f')
    c = 42.0
    res = input.scanl_last(add, c)
    exp = (input, c)
    assert res == exp

def test_scanl_last_non_empty():
    size = 111
    input = SArray.init(lambda x: 1, size)
    res = input.scanl_last(add, 0)
    exp = (SArray.init(id, size), 111)
    assert res == exp

# -------------------------- #

def test_filter_empty():
    input = SArray('f')
    res = input.filter(lambda x: x == 0.0)
    exp = input
    assert res == exp

def test_filter_non_empty():
    size = 111
    input = SArray.init(lambda x: float(x), size)
    res = input.filter(lambda x: x != 0.0)
    exp = SArray.init(lambda x: float(x+1), size-1)
    assert res == exp
