from pyske.core.list.slist import SList as SList_core
from pyske.core.runnable.list.slist import SList
import pytest


# -------------------------- #

def test_append():
    l, c = [], 1
    res = SList(l).append(c).run()
    exp = SList_core()
    exp.append(c)
    assert res == exp

# -------------------------- #

def test_head_empty():
    l = []
    res = SList(l).head().run()
    exp = SList_core(l).head()
    assert res == exp


def test_head_one():
    l = [1]
    exp = SList_core(l).head()
    res = SList(l).head().run()
    assert res == exp


def test_head_several():
    l = [1, 2]
    exp = SList_core(l).head()
    res = SList(l).head().run()
    assert res == exp


# -------------------------- #

def test_tail_empty():
    l = []
    res = SList(l).tail().run()
    exp = SList_core(l).tail()
    assert res == exp


def test_tail_one():
    l = [1]
    res = SList(l).tail().run()
    exp = SList_core(l).tail()
    assert res == exp


def test_tail_several():
    l = [1, 2, 3]
    res = SList(l).tail().run()
    exp = SList_core(l).tail()
    assert res == exp


# -------------------------- #

def test_length_nil():
    l = []
    res = SList(l).length().run()
    exp = SList_core(l).length()
    assert res == exp


def test_length_cons():
    l = [1, 2, 3]
    res = SList(l).length().run()
    exp = SList_core(l).length()
    assert res == exp


# -------------------------- #

def test_filter():
    l = [1, 2, 3, 4, 5, 6, 7, 8]
    p = lambda x: x % 2 == 0
    res = SList(l).filter(p).run()
    exp = SList_core(l).filter(p)
    assert res == exp


# -------------------------- #

def test_empty_true():
    l = []
    res = SList(l).empty().run()
    exp = SList_core(l).empty()
    assert res == exp


def test_empty_false():
    l = [1, 2, 3]
    res = SList(l).empty().run()
    exp = SList_core(l).empty()
    assert res == exp


# -------------------------- #

def test_reverse_nil():
    l = []
    res = SList(l).reverse().run()
    exp = SList_core(l).reverse()
    assert res == exp


def test_reverse_cons():
    l = [1, 2, 3]
    res = SList(l).reverse().run()
    exp = SList_core(l).reverse()
    assert res == exp


# -------------------------- #

def test_map_empty():
    l = []
    f = lambda x: x
    res = SList(l).map(f).run()
    exp = SList_core(l).map(f)
    assert res == exp


def test_map_inc():
    l = [1, 2, 3]
    f = lambda x: x
    res = SList(l).map(f).run()
    exp = SList_core(l).map(f)
    assert res == exp


def test_map_id():
    l = [1, 2, 3]
    f = lambda x: x
    res = SList(l).map(f).run()
    exp = SList_core(l).map(f)
    assert res == exp


# -------------------------- #

def test_mapi_empty():
    l = []
    f = lambda i, x: (i, x)
    res = SList(l).mapi(f).run()
    exp = SList_core(l).mapi(f)
    assert res == exp


def test_mapi_non_empty():
    l = [1, 2, 3]
    f = lambda i, x: (i, x)
    res = SList(l).mapi(f).run()
    exp = SList_core(l).mapi(f)
    assert res == exp


def test_mapi_id():
    l = [1, 2, 3]
    f = lambda i, x: x
    res = SList(l).mapi(f).run()
    exp = SList_core(l).mapi(f)
    assert res == exp

# -------------------------- #


def test_reduce_nil():
    l, e = [], 1232
    f = lambda x, y: x + y
    res = SList(l).reduce(f, e).run()
    exp = SList_core(l).reduce(f, e)
    assert res == exp


def test_reduce_cons():
    l = [1, 2, 3, 4]
    f = lambda x, y: x + y
    res = SList(l).reduce(f).run()
    exp = SList_core(l).reduce(f)
    assert res == exp


def test_reduce_sum_empty():
    l, e = [], 0
    f = lambda x, y: x + y
    res = SList(l).reduce(f, e).run()
    exp = SList_core(l).reduce(f, e)
    assert res == exp


def test_reduce_sum_non_empty():
    l, e = [1, 2, 3, 4, 5, 6], 1
    f = lambda x, y: x + y
    res = SList(l).reduce(f, e).run()
    exp = SList_core(l).reduce(f, e)
    assert res == exp


# -------------------------- #

def test_scan_nil():
    l, c = [], 0
    f = lambda x, y: x + y
    res = SList(l).scan(f, c).run()
    exp = SList_core(l).scan(f, c)
    assert res == exp


def test_scan_cons():
    l, c = [1, 2, 3, 4], 0
    f = lambda x, y: x + y
    res = SList(l).scan(f, c).run()
    exp = SList_core(l).scan(f, c)
    assert res == exp


# -------------------------- #

def test_scanr_empty():
    l = []
    f = lambda x, y: x + y
    with pytest.raises(AssertionError):
        SList(l).scanr(f).run()


def test_scanr_singleton():
    l = [1]
    f = lambda x, y: x + y
    res = SList(l).scanr(f).run()
    exp = SList_core(l).scanr(f)
    assert res == exp


def test_scanr_non_singleton():
    l = [1, 2, 3, 4]
    f = lambda x, y: x + y
    res = SList(l).scanr(f).run()
    exp = SList_core(l).scanr(f)
    assert res == exp


def test_scanr_full_distribution():
    l = [(0, 1), (1, 3), (0, 3), (0, 3), (0, 3)]

    def f(x, y):
        (x1, y1) = x
        (x2, y2) = y
        return x1 + y1, y2

    res = SList(l).scanr(f).run()
    exp = SList_core(l).scanr(f)
    assert res == exp


def test_scanr_full_distribution2():
    l = [(0, 1), (1, 3), (4, 3)]

    def f(x, y):
        (x1, y1) = x
        (x2, y2) = y
        return x1 + y1, y2

    res = SList(l).scanr(f).run()
    exp = SList_core(l).scanr(f)
    assert res == exp

# -------------------------- #


def test_scanl_empty():
    l, c = [], 0
    f = lambda x, y: x + y
    res = SList(l).scanl(f, c).run()
    exp = SList_core(l).scanl(f, c)
    assert res == exp


def test_scanl_non_empty():
    l, c = [1, 2, 3, 4], 0
    f = lambda x, y: x + y
    res = SList(l).scanl(f, c).run()
    exp = SList_core(l).scanl(f, c)
    assert res == exp

# -------------------------- #

def test_scanl_last_empty():
    l, c = [], 0
    f = lambda x, y: x + y
    res = SList(l).scanl_last(f, c).run()
    exp = SList_core(l).scanl_last(f, c)
    assert res == exp


def test_scanl_last_non_empty():
    l, c = [1, 2, 3, 4], 0
    f = lambda x, y: x + y
    res = SList(l).scanl_last(f, c).run()
    exp = SList_core(l).scanl_last(f, c)
    assert res == exp


# -------------------------- #

def test_scanp_empty():
    l, c = [], 0
    f = lambda x, y: x + y
    res = SList(l).scanp(f, c).run()
    exp = SList_core(l).scanp(f, c)
    assert res == exp


def test_scanp_non_empty():
    l, c = [1, 2, 3, 4], 0
    f = lambda x, y: x + y
    res = SList(l).scanp(f, c).run()
    exp = SList_core(l).scanp(f, c)
    assert res == exp


# -------------------------- #

def test_zip_nil():
    l1 = []
    l2 = []
    res = SList(l1).zip(SList(l2)).run()
    exp = SList_core(l1).zip(SList_core(l2))
    assert res == exp


def test_zip_cons():
    l1 = [1, 2, 3]
    l2 = [2, 3, 4]
    res = SList(l1).zip(SList(l2)).run()
    exp = SList_core(l1).zip(SList_core(l2))
    assert res == exp


def test_zip_one_gt():
    l1 = [1, 2, 3]
    l2 = [2, 3]
    with pytest.raises(AssertionError):
        SList(l1).zip(SList(l2)).run()


def test_zip_one_lt():
    l1 = [1, 2, 3]
    l2 = [2, 3]
    with pytest.raises(AssertionError):
        SList(l2).zip(SList(l1)).run()


# -------------------------- #

def test_zipwith_nil():
    l1 = []
    l2 = []
    f = lambda x, y: x + y
    res = SList(l1).map2(f, SList(l2)).run()
    exp = SList_core(l1).map2(f, SList_core(l2))
    assert res == exp


def test_zipwith_cons():
    l1 = [1, 2, 3]
    l2 = [2, 3, 4]
    f = lambda x, y: x + y
    res = SList(l1).map2(f, SList(l2)).run()
    exp = SList_core(l1).map2(f, SList_core(l2))
    assert res == exp


def test_zipwith_one_gt():
    l2 = [2, 3]
    l1 = [2, 3, 4]
    f = lambda x, y: x + y
    with pytest.raises(AssertionError):
        SList(l1).map2(f, SList(l2)).run()


def test_zipwith_one_lt():
    l1 = [2, 3]
    l2 = [2, 3, 4]
    f = lambda x, y: x + y
    with pytest.raises(AssertionError):
        SList(l1).map2(f, SList(l2)).run()

# -------------------------- #

def test_composition_empty():
    l1 = []
    l2 = []

    fm = lambda x: x + 1
    c = 0
    k = lambda x, y: x + y
    f2 = lambda x, y: x + y
    fr = lambda x, y: x - y
    f = lambda x, y: x*y
    cr = 4

    res = SList(l1).map(fm).map2(f2, SList(l2).scanp(k, c)).scanl(fr, c).reduce(f, cr).run()
    exp = SList_core(l1).map(fm).map2(f2, SList_core(l2).scanp(k, c)).scanl(fr, c).reduce(f, cr)
    assert exp == res


def test_composition_cons():
    l1 = [1, 2, 3]
    l2 = [2, 3, 4]

    fm = lambda x: x + 1
    c = 0
    k = lambda x, y: x + y
    f2 = lambda x, y: x + y
    fr = lambda x, y: x - y
    f = lambda x, y: x*y

    res = SList(l1).map(fm).map2(f2, SList(l2).scanp(k, c)).scanr(fr).reduce(f).run()
    exp = SList_core(l1).map(fm).map2(f2, SList_core(l2).scanp(k, c)).scanr(fr).reduce(f)
    assert exp == res



