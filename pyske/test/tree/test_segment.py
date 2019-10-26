import operator

import pytest

from pyske.core.support.errors import IllFormedError, ApplicationError, NotSameTagError
from pyske.core.tree.ltree import Segment, TAG_CRITICAL, TAG_LEAF, TAG_NODE
from pyske.core.util import fun


def test_has_critical_empty():
    seg = Segment()
    exp = False
    res = seg.has_critical()
    assert exp == res


def test_has_critical_no():
    val1 = (1, TAG_NODE)
    val2 = (2, TAG_LEAF)
    seg = Segment([val1, val2])
    exp = False
    res = seg.has_critical()
    assert exp == res


def test_has_critical_yes():
    val1 = (1, TAG_NODE)
    val2 = (2, TAG_LEAF)
    val3 = (3, TAG_CRITICAL)
    seg = Segment([val1, val2, val3])
    exp = True
    res = seg.has_critical()
    assert exp == res


# -------------------------- #

def test_map_local_empty():
    seg = Segment()
    res = seg.map_local(lambda x: x + 1, lambda x: x - 1)
    exp = Segment()
    assert exp == res


def test_map_local():
    seg = Segment([(1, TAG_NODE), (2, TAG_LEAF), (3, TAG_CRITICAL)])
    res = seg.map_local(lambda x: x + 1, lambda x: x - 1)
    exp = Segment([(0, TAG_NODE), (3, TAG_LEAF), (2, TAG_CRITICAL)])
    assert exp == res


# -------------------------- #

def test_reduce_local_empty():
    seg = Segment()
    with pytest.raises(AssertionError):
        seg.reduce_local(fun.add, fun.idt, fun.add, fun.add)


def test_reduce_local_illformed():
    seg = Segment([(1, TAG_NODE), (2, TAG_CRITICAL)])
    with pytest.raises(IllFormedError):
        seg.reduce_local(fun.add, fun.idt, fun.add, fun.add)


def test_reduce_local_node():
    seg = Segment([(1, TAG_NODE), (2, TAG_LEAF), (3, TAG_CRITICAL)])
    res = seg.reduce_local(fun.add, fun.idt, fun.add, fun.add)
    exp = (6, TAG_NODE)
    assert res == exp


def test_reduce_local_leaf():
    seg = Segment([(1, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    res = seg.reduce_local(fun.add, fun.idt, fun.add, fun.add)
    exp = (6, TAG_LEAF)
    assert res == exp


# -------------------------- #

def test_reduce_global_has_critical():
    seg = Segment([(1, TAG_NODE), (2, TAG_LEAF), (2, TAG_CRITICAL)])
    with pytest.raises(AssertionError):
        seg.reduce_global(fun.add)


def test_reduce_global_empty():
    seg = Segment()
    with pytest.raises(AssertionError):
        seg.reduce_global(fun.add)


def test_reduce_global_illformed():
    seg = Segment([(1, TAG_NODE), (2, TAG_LEAF)])
    with pytest.raises(IllFormedError):
        seg.reduce_global(fun.add)


def test_reduce_global_leaf():
    seg = Segment([(2, TAG_LEAF)])
    res = seg.reduce_global(fun.add)
    exp = 2
    assert res == exp


def test_reduce_global_node():
    seg = Segment([(2, TAG_NODE), (2, TAG_LEAF), (2, TAG_LEAF)])
    res = seg.reduce_global(fun.add)
    exp = 6
    assert res == exp


# -------------------------- #

def test_uacc_local_empty():
    seg = Segment()
    with pytest.raises(AssertionError):
        seg.uacc_local(fun.add, fun.idt, fun.add, fun.add)


def test_uacc_local_illformed():
    seg = Segment([(1, TAG_NODE), (2, TAG_CRITICAL)])
    with pytest.raises(IllFormedError):
        seg.uacc_local(fun.add, fun.idt, fun.add, fun.add)


def test_uacc_local_node():
    seg = Segment(
        [(1, TAG_NODE), (2, TAG_LEAF), (1, TAG_NODE), (2, TAG_LEAF), (3, TAG_CRITICAL)])
    res = seg.uacc_local(fun.add, fun.idt, fun.add, fun.add)
    exp = ((9, TAG_NODE), Segment([(None, TAG_NODE), (2, TAG_LEAF), (None, TAG_NODE), (2, TAG_LEAF), (None, TAG_CRITICAL)]))
    assert res == exp


def test_uacc_local_leaf():
    seg = Segment(
        [(1, TAG_NODE), (2, TAG_LEAF), (1, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    res = seg.uacc_local(fun.add, fun.idt, fun.add, fun.add)
    exp = ((9, TAG_LEAF), Segment(
        [(9, TAG_NODE), (2, TAG_LEAF), (6, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)]))
    assert res == exp


# -------------------------- #
def phi(_):
    return 1, 0, 0, 1


def k(l, _, r):
    ll, ls = l
    rl, rs = r
    return ls, ls + 1 + rs


def psi_l(l, b, r):
    l0, l1, l2, l3 = l
    b0, b1, b2, b3 = b
    rl, rs = r
    res_0 = 0
    res_1 = b0 + b1
    res_2 = (b0 + b1) * l3 + b1 * (1 + rs) + b2
    res_3 = l3 + 1 + rs + b3
    return res_0, res_1, res_2, res_3


def psi_r(l, b, r):
    ll, ls = l
    b0, b1, b2, b3 = b
    r0, r1, r2, r3 = r
    res_0 = 0
    res_1 = b1
    res_2 = b1 * r3 + b0 * ls + b1 * (1 + ls) + b2
    res_3 = r3 + 1 + ls + b3
    return res_0, res_1, res_2, res_3


def psi_n(l, b, r):
    ll, ls = l
    b0, b1, b2, b3 = b
    rl, rs = r
    res_1 = b0 * ls + b1 * (ls + rs + 1) + b2
    res_2 = ls + 1 + rs + b3
    return res_1, res_2


def test_uacc_local_prefix_1():
    seg = Segment([(1, TAG_NODE), (2, TAG_CRITICAL), ((0, 1), TAG_LEAF)])
    res = seg.uacc_local(k, phi, psi_l, psi_r)
    exp = (((0, 1, 1, 4), TAG_NODE), Segment([(None, TAG_NODE), (None, TAG_CRITICAL), ((0, 1), TAG_LEAF)]))
    assert res == exp


def test_uacc_local_prefix_2():
    seg = Segment([(4, TAG_NODE), ((0, 1), TAG_LEAF), ((0, 1), TAG_LEAF)])
    res = seg.uacc_local(k, phi, psi_l, psi_r)
    exp = (((1, 3), TAG_LEAF),
           Segment([((1, 3), TAG_NODE),
                    ((0, 1), TAG_LEAF),
                    ((0, 1), TAG_LEAF)]))
    assert res == exp


def test_uacc_local_prefix_3():
    seg = Segment([(5, TAG_NODE), ((0, 1), TAG_LEAF), ((0, 1), TAG_LEAF)])
    res = seg.uacc_local(k, phi, psi_l, psi_r)
    exp = (
        ((1, 3), TAG_LEAF),
        Segment([((1, 3), TAG_NODE), ((0, 1), TAG_LEAF), ((0, 1), TAG_LEAF)]))
    assert res == exp


def test_uacc_global_prefix():
    gt = Segment([((0, 1, 1, 4), TAG_NODE), ((1, 3), TAG_LEAF), ((1, 3), TAG_LEAF)])
    res = gt.uacc_global(psi_n)
    exp = Segment([((8, 11), TAG_NODE), ((1, 3), TAG_LEAF), ((1, 3), TAG_LEAF)])
    assert res == exp


def test_uacc_update_prefix():
    seg = Segment([(1, TAG_NODE), (2, TAG_CRITICAL), ((0, 1), TAG_LEAF)])
    seg2 = Segment([(None, None), (None, None), ((0, 1), TAG_LEAF)])
    lc = (1, 3)
    rc = (1, 3)
    res = seg.uacc_update(seg2, k, lc, rc)
    exp = Segment([((5, 9), TAG_NODE), ((1, 5), TAG_CRITICAL), ((0, 1), TAG_LEAF)])
    assert res == exp


# -------------------------- #

def test_uacc_global_has_critical():
    seg = Segment([(1, TAG_NODE), (2, TAG_CRITICAL), (2, TAG_LEAF)])
    with pytest.raises(AssertionError):
        seg.uacc_global(fun.add)


def test_uacc_global_empty():
    seg = Segment()
    exp = Segment()
    res = seg.uacc_global(fun.add)
    assert exp == res


def test_uacc_global_illformed():
    seg = Segment([(1, TAG_NODE), (2, TAG_LEAF)])
    with pytest.raises(IllFormedError):
        seg.uacc_global(fun.add)


def test_uacc_global_leaf():
    seg = Segment([(3, TAG_LEAF)])
    res = seg.uacc_global(fun.add)
    exp = Segment([(3, TAG_LEAF)])
    assert res == exp


def test_uacc_global_node():
    seg = Segment(
        [(1, TAG_NODE), (2, TAG_LEAF), (1, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    res = seg.uacc_global(fun.add)
    exp = Segment(
        [(9, TAG_NODE), (2, TAG_LEAF), (6, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    assert res == exp


# -------------------------- #

def test_uacc_update_empty():
    seg = Segment()
    gt = Segment()
    lc = 1
    rc = 2
    res = seg.uacc_update(gt, fun.add, lc, rc)
    exp = Segment()
    assert res == exp


def test_uacc_update_not_same_size():
    seg = Segment(
        [(1, TAG_NODE), (2, TAG_LEAF), (1, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    gt = Segment()
    lc = 1
    rc = 2
    with pytest.raises(AssertionError):
        seg.uacc_update(gt, fun.add, lc, rc)


def test_uacc_update_illformed_node():
    seg = Segment([(1, TAG_NODE), (2, TAG_NODE), (2, TAG_NODE)])
    gt = Segment([(1, TAG_NODE), (2, TAG_LEAF), (2, TAG_LEAF)])
    lc = 1
    rc = 2
    with pytest.raises(IllFormedError):
        seg.uacc_update(gt, fun.add, lc, rc)


def test_uacc_update_illformed_critical():
    seg = Segment([(1, TAG_NODE), (2, TAG_CRITICAL), (1, TAG_NODE)])
    gt = Segment([(1, TAG_NODE), (2, TAG_LEAF), (1, TAG_LEAF)])
    lc = 1
    rc = 2
    with pytest.raises(IllFormedError):
        seg.uacc_update(gt, fun.add, lc, rc)


def test_uacc_update_leaf():
    seg = Segment(
        [(1, TAG_NODE), (2, TAG_LEAF), (1, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    gt = Segment(
        [(9, TAG_NODE), (2, TAG_LEAF), (6, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    lc = 1
    rc = 2
    res = seg.uacc_update(gt, fun.add, lc, rc)
    exp = Segment(
        [(9, TAG_NODE), (2, TAG_LEAF), (6, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    assert res == exp


def test_uacc_update_node():
    seg = Segment(
        [(1, TAG_NODE), (2, TAG_LEAF), (1, TAG_NODE), (2, TAG_LEAF), (3, TAG_CRITICAL)])
    gt = Segment(
        [(1, TAG_NODE), (2, TAG_LEAF), (1, TAG_NODE), (2, TAG_LEAF), (3, TAG_CRITICAL)])
    lc = 1
    rc = 2
    res = seg.uacc_update(gt, fun.add, lc, rc)
    exp = Segment(
        [(12, TAG_NODE), (2, TAG_LEAF), (9, TAG_NODE), (2, TAG_LEAF), (6, TAG_CRITICAL)])
    assert res == exp


# -------------------------- #

def test_dacc_path_empty():
    seg = Segment()
    with pytest.raises(AssertionError):
        seg.dacc_path(fun.idt, fun.idt, operator.add)


def test_dacc_path_has_no_critical():
    seg = Segment([(1, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    with pytest.raises(ApplicationError):
        seg.dacc_path(fun.idt, fun.idt, operator.add)


def test_dacc_path_gt_node():
    seg = Segment(
        [(1, TAG_NODE), (2, TAG_LEAF), (1, TAG_NODE), (2, TAG_LEAF), (3, TAG_CRITICAL)])
    res = seg.dacc_path(fun.idt, fun.idt, operator.add)
    exp = ((5, 5), TAG_NODE)
    assert res == exp


# -------------------------- #

def test_dacc_global_double_leaf():
    seg = Segment([(1, TAG_LEAF), (1, TAG_LEAF)])
    c = 2
    with pytest.raises(IllFormedError):
        seg.dacc_global(operator.add, c)


def test_dacc_global_empty():
    seg = Segment()
    c = 2
    res = seg.dacc_global(operator.add, c)
    exp = Segment()
    assert res == exp


def test_dacc_global_has_critical():
    seg = Segment([(1, TAG_NODE), (1, TAG_CRITICAL), (1, TAG_LEAF)])
    c = 2
    with pytest.raises(AssertionError):
        seg.dacc_global(operator.add, c)


def test_dacc_global():
    c = 2
    seg = Segment(
        [((1, 1), TAG_NODE), ((2, 3), TAG_LEAF), ((1, 2), TAG_NODE), ((2, 2), TAG_LEAF),
         ((3, 1), TAG_LEAF)])
    res = seg.dacc_global(operator.add, c)
    exp = Segment(
        [(2, TAG_NODE), (3, TAG_LEAF), (3, TAG_NODE), (4, TAG_LEAF), (5, TAG_LEAF)])
    assert res == exp


# -------------------------- #

def test_dacc_local_empty():
    seg = Segment()
    c = 4
    res = seg.dacc_local(operator.add, operator.add, c)
    exp = Segment()
    assert res == exp


def test_dacc_local_stack_empty_leaf():
    seg = Segment([(2, TAG_LEAF), (2, TAG_LEAF)])
    c = 4
    with pytest.raises(IllFormedError):
        seg.dacc_local(operator.add, operator.add, c)


def test_dacc_local_stack_empty_critical():
    seg = Segment([(2, TAG_CRITICAL), (2, TAG_LEAF)])
    c = 4
    with pytest.raises(IllFormedError):
        seg.dacc_local(operator.add, operator.add, c)


def test_dacc_local():
    seg = Segment([(231, TAG_NODE), (169, TAG_LEAF), (478, TAG_NODE), (634, TAG_LEAF),
                   (2, TAG_CRITICAL)])
    c = 400
    res = seg.dacc_local(operator.add, operator.sub, c)
    exp = Segment([(400, TAG_NODE), (631, TAG_LEAF), (169, TAG_NODE), (647, TAG_LEAF),
                   (-309, TAG_CRITICAL)])
    assert res == exp


# -------------------------- #

def test_get_left_has_critical():
    gt = Segment([(2, TAG_NODE), (1, TAG_CRITICAL), (2, TAG_LEAF)])
    i = 0
    with pytest.raises(AssertionError):
        gt.get_left(i)


def test_get_left_is_leaf():
    gt = Segment([(2, TAG_NODE), (1, TAG_LEAF), (2, TAG_LEAF)])
    i = 1
    with pytest.raises(AssertionError):
        gt.get_left(i)


def test_get_left_illformed():
    gt = Segment([(2, TAG_NODE)])
    i = 0
    with pytest.raises(AssertionError):
        gt.get_left(i)


def test_get_left():
    gt = Segment([(2, TAG_NODE), (1, TAG_LEAF), (2, TAG_LEAF)])
    i = 0
    res = gt.get_left(i)
    exp = (1, TAG_LEAF)
    assert res == exp


# -------------------------- #

def test_get_right_has_critical():
    gt = Segment([(2, TAG_NODE), (1, TAG_CRITICAL), (2, TAG_LEAF)])
    i = 0
    with pytest.raises(AssertionError):
        gt.get_right(i)


def test_get_right_is_leaf():
    gt = Segment([(2, TAG_NODE), (1, TAG_LEAF), (2, TAG_LEAF)])
    i = 1
    with pytest.raises(AssertionError):
        gt.get_right(i)


def test_get_right_illformed():
    gt = Segment([(2, TAG_NODE), (1, TAG_LEAF)])
    i = 0
    with pytest.raises(AssertionError):
        gt.get_right(i)


def test_get_right_direct():
    gt = Segment([(2, TAG_NODE), (1, TAG_LEAF), (2, TAG_LEAF)])
    i = 0
    res = gt.get_right(i)
    exp = (2, TAG_LEAF)
    assert res == exp


def test_get_right_not_direct():
    gt = Segment(
        [(1, TAG_NODE), (3, TAG_NODE), (8, TAG_LEAF), (4, TAG_LEAF), (2, TAG_LEAF)])
    i = 0
    res = gt.get_right(i)
    exp = (2, TAG_LEAF)
    assert res == exp


# -------------------------- #

def test_zip_local_not_equal_size_error():
    seg1 = Segment([(2, TAG_NODE), (1, TAG_LEAF), (2, TAG_LEAF)])
    seg2 = Segment([(2, TAG_LEAF)])
    with pytest.raises(AssertionError):
        seg1.zip_local(seg2)


def test_zip_local_not_same_tag_error():
    seg1 = Segment([(2, TAG_NODE), (1, TAG_LEAF), (2, TAG_LEAF)])
    seg2 = Segment([(2, TAG_NODE), (1, TAG_CRITICAL), (2, TAG_LEAF)])
    with pytest.raises(NotSameTagError):
        seg1.zip_local(seg2)


def test_zip_local():
    seg1 = Segment([(1, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    seg2 = Segment([(4, TAG_NODE), (5, TAG_LEAF), (6, TAG_LEAF)])
    res = seg1.zip_local(seg2)
    exp = Segment([((1, 4), TAG_NODE), ((2, 5), TAG_LEAF), ((3, 6), TAG_LEAF)])
    assert res == exp


# -------------------------- #


def test_zip_localwith_not_equal_size_error():
    seg1 = Segment([(2, TAG_NODE), (1, TAG_LEAF), (2, TAG_LEAF)])
    seg2 = Segment([(2, TAG_LEAF)])
    with pytest.raises(AssertionError):
        seg1.map2_local(operator.add, operator.add, seg2)


def test_zip_localwith_not_same_tag_error():
    seg1 = Segment([(2, TAG_NODE), (1, TAG_LEAF), (2, TAG_LEAF)])
    seg2 = Segment([(2, TAG_NODE), (1, TAG_CRITICAL), (2, TAG_LEAF)])
    with pytest.raises(NotSameTagError):
        seg1.map2_local(operator.add, operator.add, seg2)


def test_zip_localwith():
    seg1 = Segment([(1, TAG_NODE), (2, TAG_LEAF), (3, TAG_LEAF)])
    seg2 = Segment([(4, TAG_NODE), (5, TAG_LEAF), (6, TAG_LEAF)])
    res = seg1.map2_local(operator.add, operator.add, seg2)
    exp = Segment([(5, TAG_NODE), (7, TAG_LEAF), (9, TAG_LEAF)])
    assert res == exp
