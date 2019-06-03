from pyske.core.support.errors import NotEqualSizeError, EmptyError
from pyske.core.list.slist import SList
from pyske.core.runnable.list.eslist import ESList
import pytest


# -------------------------- #

def test_head_empty():
    sl = SList()
    sl_run = ESList(sl)
    sl_run.head()
    res = sl_run.run()
    exp = sl.head()
    assert res == exp


def test_head_one():
    sl = SList()
    exp = 1
    sl.append(exp)
    sl_run = ESList(sl)
    sl_run.head()
    res = sl_run.run()
    assert res == exp


def test_head_several():
    sl = SList()
    exp = 1
    sl.append(exp)
    sl.append(exp + 1)
    sl_run = ESList(sl)
    sl_run.head()
    res = sl_run.run()
    assert res == exp


# -------------------------- #

def test_tail_empty():
    sl = SList()
    sl_run = ESList(sl)
    sl_run.tail()
    res = sl_run.run()
    exp = sl.tail()
    assert res == exp


def test_tail_one():
    sl = SList([1])
    sl_run = ESList(sl)
    sl_run.tail()
    res = sl_run.run()
    exp = sl.tail()
    assert res == exp


def test_tail_several():
    sl = SList([1, 2, 3])
    sl_run = ESList(sl)
    sl_run.tail()
    res = sl_run.run()
    exp = sl.tail()
    assert res == exp


# -------------------------- #

def test_length_nil():
    sl = SList()
    sl_run = ESList(sl)
    sl_run.length()
    res = sl_run.run()
    exp = sl.length()
    assert res == exp


def test_length_cons():
    sl = SList([1, 2, 3])
    sl_run = ESList(sl)
    sl_run.length()
    res = sl_run.run()
    exp = sl.length()
    assert res == exp


# -------------------------- #

def test_filter():
    sl = SList([1, 2, 3, 4, 5, 6, 7, 8])
    sl_run = ESList(sl)
    p = lambda x: x % 2 == 0
    sl_run.filter(p)
    res = sl_run.run()
    exp = sl.filter(p)
    assert res == exp


# -------------------------- #

def test_empty_true():
    sl = SList()
    sl_run = ESList(sl)
    sl_run.empty()
    res = sl_run.run()
    exp = sl.empty()
    assert res == exp


def test_empty_false():
    sl = SList([1, 2, 3])
    sl_run = ESList(sl)
    sl_run.empty()
    res = sl_run.run()
    exp = sl.empty()
    assert res == exp


# -------------------------- #

def test_reverse_nil():
    sl = SList()
    sl_run = ESList(sl)
    sl_run.reverse()
    res = sl_run.run()
    exp = sl.reverse()
    assert res == exp


def test_reverse_cons():
    sl = SList([1, 2, 3])
    sl_run = ESList(sl)
    sl_run.reverse()
    res = sl_run.run()
    exp = sl.reverse()
    assert res == exp


# -------------------------- #

def test_map_empty():
    sl = SList()
    sl_run = ESList(sl)
    f = lambda x: x
    sl_run.map(f)
    res = sl_run.run()
    exp = sl.map(f)
    assert res == exp


def test_map_inc():
    sl = SList([1, 2, 3])
    sl_run = ESList(sl)
    f = lambda x: x + 1
    sl_run.map(f)
    res = sl_run.run()
    exp = sl.map(f)
    assert res == exp


def test_map_id():
    sl = SList([1, 2, 3])
    sl_run = ESList(sl)
    f = lambda x: x
    exp = sl.map(f)
    sl_run.map(f)
    res = sl_run.run()
    assert res == exp


# -------------------------- #

def test_mapi_empty():
    sl = SList()
    sl_run = ESList(sl)
    f = lambda i, x: (i, x)
    sl_run.mapi(f)
    res = sl_run.run()
    exp = sl.mapi(f)
    assert res == exp


def test_mapi_non_empty():
    sl = SList([1, 2, 3])
    sl_run = ESList(sl)
    f = lambda i, x: i * x
    sl_run.mapi(f)
    res = sl_run.run()
    exp = sl.mapi(f)
    assert res == exp


def test_mapi_id():
    sl = SList([1, 2, 3])
    sl_run = ESList(sl)
    f = lambda i, x: x
    sl_run.mapi(f)
    res = sl_run.run()
    exp = sl.mapi(f)
    assert res == exp

# -------------------------- #


def test_reduce_nil():
    e = 1232
    sl = SList()
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    sl_run.reduce(f, e)
    res = sl_run.run()
    exp = sl.reduce(f, e)
    assert res == exp


def test_reduce_cons():
    sl = SList([1, 2, 3, 4])
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    sl_run.reduce(f)
    res = sl_run.run()
    exp = sl.reduce(f)
    assert res == exp


def test_reduce_sum_empty():
    e = 0
    sl = SList()
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    sl_run.reduce(f, e)
    res = sl_run.run()
    exp = sl.reduce(f, e)
    assert res == exp


def test_reduce_sum_non_empty():
    e = 1
    sl = SList([1, 2, 3, 4, 5, 6])
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    sl_run.reduce(f, e)
    res = sl_run.run()
    exp = sl.reduce(f, e)
    assert res == exp


# -------------------------- #

def test_scan_nil():
    c = 0
    sl = SList()
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    sl_run.scan(f, c)
    res = sl_run.run()
    exp = sl.scan(f, c)
    assert res == exp


def test_scan_cons():
    c = 0
    sl = SList([1, 2, 3, 4])
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    sl_run.scan(f, c)
    res = sl_run.run()
    exp = sl.scan(f, c)
    assert res == exp


# -------------------------- #

def test_scanr_empty():
    with pytest.raises(AssertionError):
        sl = SList()
        sl_run = ESList(sl)
        f = lambda x, y: x + y
        sl_run.scanr(f)
        sl_run.run()


def test_scanr_singleton():
    sl = SList([1])
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    exp = sl.scanr(f)
    sl_run.scanr(f)
    res = sl_run.run()
    assert res == exp


def test_scanr_non_singleton():
    sl = SList([1, 2, 3, 4])
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    exp = sl.scanr(f)
    sl_run.scanr(f)
    res = sl_run.run()
    assert res == exp


def test_scanr_full_distribution():
    sl = SList([(0, 1), (1, 3), (0, 3), (0, 3), (0, 3)])
    sl_run = ESList(sl)

    def f(x, y):
        (x1, y1) = x
        (x2, y2) = y
        return x1 + y1, y2

    exp = sl.scanr(f)
    sl_run.scanr(f)
    res = sl_run.run()
    assert res == exp


def test_scanr_full_distribution2():
    sl = SList([(0, 1), (1, 3), (4, 3)])
    sl_run = ESList(sl)

    def f(x, y):
        (x1, y1) = x
        (x2, y2) = y
        return x1 + y1, y2

    exp = sl.scanr(f)
    sl_run.scanr(f)
    res = sl_run.run()
    assert res == exp

# -------------------------- #


def test_scanl_empty():
    c = 0
    sl = SList([])
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    exp = sl.scanl(f, c)
    sl_run.scanl(f, c)
    res = sl_run.run()
    assert res == exp


def test_scanl_non_empty():
    c = 0
    sl = SList([1, 2, 3, 4])
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    exp = sl.scanl(f, 0)
    sl_run.scanl(f, c)
    res = sl_run.run()
    assert res == exp

# -------------------------- #

def test_scanl_last_empty():
    c = 0
    sl = SList([])
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    exp = sl.scanl_last(f, c)
    sl_run.scanl_last(f, c)
    res = sl_run.run()
    assert res == exp


def test_scanl_last_non_empty():
    c = 0
    sl = SList([1, 2, 3, 4])
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    exp = sl.scanl_last(f, c)
    sl_run.scanl_last(f, c)
    res = sl_run.run()
    assert res == exp


# -------------------------- #

def test_scanp_nil():
    c = 0
    sl = SList()
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    exp = sl.scanp(f, c)
    sl_run.scanp(f, c)
    res = sl_run.run()
    assert res == exp

def test_scanp_cons():
    c = 0
    sl = SList([1, 2, 3, 4])
    sl_run = ESList(sl)
    f = lambda x, y: x + y
    exp = sl.scanp(f, c)
    sl_run.scanp(f, c)
    res = sl_run.run()
    assert res == exp


# -------------------------- #

def test_zip_nil():
    sl1 = SList()
    sl2 = SList()
    sl1_run = ESList(sl1)
    sl2_run = ESList(sl2)
    exp = sl1.zip(sl2)
    sl1_run.zip(sl2_run)
    res = sl1_run.run()
    assert res == exp


def test_zip_cons():
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3, 4])
    sl1_run = ESList(sl1)
    sl2_run = ESList(sl2)
    exp = sl1.zip(sl2)
    sl1_run.zip(sl2_run)
    res = sl1_run.run()
    assert res == exp


def test_zip_one_gt():
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3])
    sl1_run = ESList(sl1)
    sl2_run = ESList(sl2)
    with pytest.raises(AssertionError):
        sl1_run.zip(sl2_run)
        res = sl1_run.run()


def test_zip_one_lt():
    sl1 = SList([2, 3])
    sl2 = SList([2, 3, 4])
    sl1_run = ESList(sl1)
    sl2_run = ESList(sl2)
    with pytest.raises(AssertionError):
        sl1_run.zip(sl2_run)
        res = sl1_run.run()


# -------------------------- #

def test_zipwith_nil():
    sl1 = SList()
    sl2 = SList()
    sl1_run = ESList(sl1)
    sl2_run = ESList(sl2)
    f = lambda x, y: x + y
    exp = sl1.map2(f, sl2)
    sl1_run.map2(f, sl2_run)
    res = sl1_run.run()
    assert res == exp


def test_zipwith_cons():
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3, 4])
    sl1_run = ESList(sl1)
    sl2_run = ESList(sl2)
    f = lambda x, y: x + y
    exp = sl1.map2(f, sl2)
    sl1_run.map2(f, sl2_run)
    res = sl1_run.run()
    assert res == exp


def test_zipwith_one_gt():
    sl1 = SList([1, 2, 3])
    sl2 = SList([2, 3])
    sl1_run = ESList(sl1)
    sl2_run = ESList(sl2)
    f = lambda x, y: x + y
    with pytest.raises(AssertionError):
        sl1_run.map2(f, sl2_run)
        res = sl1_run.run()


def test_zipwith_one_lt():
    sl1 = SList([2, 3])
    sl2 = SList([2, 3, 4])
    sl1_run = ESList(sl1)
    sl2_run = ESList(sl2)
    f = lambda x, y: x + y
    with pytest.raises(AssertionError):
        sl1_run.map2(f, sl2_run)
        res = sl1_run.run()


