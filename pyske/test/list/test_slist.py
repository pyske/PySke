import pytest
from pyske.core.util import fun
from pyske.core.list.slist import SList
import operator

# -------------------------- #


def test_head_empty():
    sl = SList()
    exp = None
    res = sl.head()
    assert res == exp


def test_head_one():
    sl = SList()
    exp = 1
    sl.append(exp)
    res = sl.head()
    assert res == exp


def test_head_several():
    sl = SList()
    exp = 1
    sl.append(exp)
    sl.append(exp + 1)
    res = sl.head()
    assert res == exp


# -------------------------- #

def test_tail_empty():
    sl = SList()
    exp = SList()
    res = sl.tail()
    assert res == exp


def test_tail_one():
    sl = SList([1])
    exp = SList()
    res = sl.tail()
    assert res == exp


def test_tail_several():
    sl = SList([1, 2, 3])
    exp = SList([2, 3])
    res = sl.tail()
    assert res == exp


# -------------------------- #

def test_length_nil():
    sl = SList()
    exp = 0
    res = sl.length()
    assert res == exp


def test_length_cons():
    sl = SList([1, 2, 3])
    exp = 3
    res = sl.length()
    assert res == exp


# -------------------------- #

def test_filter():
    sl = SList([1, 2, 3, 4, 5, 6, 7, 8])
    res = sl.filter(lambda x: x % 2 == 0)
    for r in res:
        assert r % 2 == 0


# -------------------------- #

def test_empty_true():
    sl = SList()
    exp = True
    res = sl.empty()
    assert res == exp


def test_empty_false():
    sl = SList([1, 2, 3])
    exp = False
    res = sl.empty()
    assert res == exp


# -------------------------- #

def test_map_empty():
    sl = SList()
    exp = SList()
    res = sl.map(fun.idt)
    assert res == exp


def test_map_inc():
    sl = SList([1, 2, 3])
    exp = SList([2, 3, 4])
    res = sl.map(fun.incr)
    assert res == exp


def test_map_id():
    sl = SList([1, 2, 3])
    exp = SList([1, 2, 3])
    res = sl.map(fun.idt)
    assert res == exp


# -------------------------- #

def test_mapi_empty():
    sl = SList()
    exp = SList()
    res = sl.mapi(lambda i, x: (i, x))
    assert res == exp


def test_mapi_non_empty():
    sl = SList([1, 2, 3])
    exp = SList([0, 2, 6])
    res = sl.mapi(operator.mul)
    assert res == exp


def test_mapi_id():
    sl = SList([1, 2, 3])
    exp = SList([1, 2, 3])
    res = sl.mapi(lambda i, x: x)
    assert res == exp


# -------------------------- #

def test_map_reduce_nil():
    e = 1232
    sl = SList()
    res = sl.map_reduce(fun.incr, operator.add, e)
    exp = e
    assert res == exp


def test_map_reduce_cons():
    sl = SList([1, 2, 3, 4])
    res = sl.map_reduce(fun.incr, operator.add)
    exp = sl.map(fun.incr).reduce(operator.add)
    assert res == exp


# -------------------------- #


def test_reduce_nil():
    e = 1232
    sl = SList()
    res = sl.reduce(operator.add, e)
    exp = e
    assert res == exp


def test_reduce_cons():
    sl = SList([1, 2, 3, 4])
    res = sl.reduce(operator.add)
    exp = 10
    assert res == exp


def test_reduce_sum_empty():
    sl = SList()
    exp = 0
    res = sl.reduce(operator.add, 0)
    assert res == exp


def test_reduce_sum_non_empty():
    sl = SList([1, 2, 3, 4, 5, 6])
    exp = 22
    res = sl.reduce(operator.add, 1)
    assert res == exp


# -------------------------- #

def test_scan_nil():
    c = 0
    sl = SList()
    res = sl.scan(operator.add, c)
    exp = SList([0])
    assert res == exp


def test_scan_cons():
    c = 0
    sl = SList([1, 2, 3, 4])
    res = sl.scan(operator.add, c)
    exp = SList([0, 1, 3, 6, 10])
    assert res == exp


# -------------------------- #

def test_scanr_empty():
    with pytest.raises(AssertionError):
        sl = SList()
        sl.scanr(operator.add)


def test_scanr_singleton():
    sl = SList([1])
    res = sl.scanr(operator.add)
    assert res == sl


def test_scanr_non_singleton():
    sl = SList([1, 2, 3, 4])
    res = sl.scanr(operator.add)
    exp = SList([1, 3, 6, 10])
    assert res == exp


def test_scanr_full_distribution():
    sl = SList([(0, 1), (1, 3), (0, 3), (0, 3), (0, 3)])

    def f(x, y):
        (x1, y1) = x
        (x2, y2) = y
        return x1 + y1, y2

    res = sl.scanr(f)
    exp = SList([(0, 1), (1, 3), (4, 3), (7, 3), (10, 3)])
    assert res == exp


def test_scanr_full_distribution2():
    sl = SList([(0, 1), (1, 3), (4, 3)])

    def f(x, y):
        (x1, y1) = x
        (x2, y2) = y
        return x1 + y1, y2

    res = sl.scanr(f)
    exp = SList([(0, 1), (1, 3), (4, 3)])
    assert res == exp


# -------------------------- #

def test_scanl_empty():
    sl = SList([])
    res = sl.scanl(operator.add, 0)
    exp = SList([])
    assert res == exp


def test_scanl_non_empty():
    sl = SList([1, 2, 3, 4])
    res = sl.scanl(operator.add, 0)
    exp = SList([0, 1, 3, 6])
    assert res == exp


# -------------------------- #

def test_scanl_last_empty():
    sl = SList([])
    res = sl.scanl_last(operator.add, 0)
    exp = ([], 0)
    assert res == exp


def test_scanl_last_non_empty():
    sl = SList([1, 2, 3, 4])
    res = sl.scanl_last(operator.add, 0)
    exp = (SList([0, 1, 3, 6]), 10)
    assert res == exp


# -------------------------- #

def test_scanp_nil():
    c = 0
    sl = SList()
    res = sl.scanp(operator.add, c)
    exp = SList([])
    assert res == exp


def test_scanp_cons():
    c = 0
    sl = SList([1, 2, 3, 4])
    res = sl.scanp(operator.add, c)
    exp = SList([9, 7, 4, 0])
    assert res == exp


# -------------------------- #

def test_zip_nil():
    sl1 = SList()
    sl2 = SList()
    res = sl1.zip(sl2)
    exp = SList()
    assert res == exp


def test_zip_cons():
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3, 4])
    res = sl1.zip(sl2)
    exp = SList([(1, 2), (2, 3), (3, 4)])
    assert res == exp


def test_zip_one_gt():
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3])
    with pytest.raises(AssertionError):
        sl1.zip(sl2)


def test_zip_one_lt():
    sl1 = SList([2, 3])
    sl2 = SList([2, 3, 4])
    with pytest.raises(AssertionError):
        sl1.zip(sl2)


# -------------------------- #

def test_zipwith_nil():
    sl1 = SList()
    sl2 = SList()
    res = sl1.map2(operator.add, sl2)
    exp = SList()
    assert res == exp


def test_zipwith_cons():
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3, 4])
    res = sl1.map2(operator.add, sl2)
    exp = SList([3, 5, 7])
    assert res == exp


def test_zipwith_one_gt():
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3])
    with pytest.raises(AssertionError):
        sl1.map2(operator.add, sl2)


def test_zipwith_one_lt():
    sl1 = SList([2, 3])
    sl2 = SList([2, 3, 4])
    with pytest.raises(AssertionError):
        sl1.map2(operator.add, sl2)


# -------------------------- #

def test_from_str_simple():
    s = "[1;2;3]"
    res = SList.from_str(s)
    exp = SList([1, 2, 3])
    assert res == exp


def parser_tuple(s):
    s = s.replace("(", "")
    s = s.replace(")", "")
    ss = s.split(",")
    return int(ss[0]), int(ss[1])


def test_from_str_tuple():
    s = "[(1,2);(3,4)]"
    res = SList.from_str(s, parser=parser_tuple)
    exp = SList([(1, 2), (3, 4)])
    assert res == exp

# -------------------------- #
