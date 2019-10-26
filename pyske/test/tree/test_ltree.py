import operator

import pytest

from pyske.core.support.errors import IllFormedError
from pyske.core.tree.btree import Leaf, Node
from pyske.core.tree.ltree import LTree, Segment, TAG_LEAF, TAG_NODE, TAG_CRITICAL
from pyske.core.util import fun


# -------------------------- #


def test_map_empty():
    lt = LTree()
    with pytest.raises(AssertionError):
        lt.map(fun.idt, fun.idt)


def test_map_leaf():
    bt = Leaf(1)
    res = LTree.init_from_bt(bt, 1).map(lambda x: x + 1, lambda x: x - 1)
    exp = LTree.init_from_bt(Leaf(2), 1)
    assert exp == res


def test_map_node():
    bt = Node(1, Leaf(2), Leaf(3))
    res = LTree.init_from_bt(bt, 1).map(fun.incr, fun.decr)
    exp = LTree.init_from_bt(Node(0, Leaf(3), Leaf(4)), 1)
    assert exp == res

# -------------------------- #


def test_reduce_empty():
    lt = LTree()
    with pytest.raises(AssertionError):
        lt.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add)


def test_reduce_illformed():
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg3 = Segment([(72, TAG_NODE), (92, TAG_LEAF), (42, TAG_LEAF)])
    lt = LTree([seg1, seg3])
    with pytest.raises(IllFormedError):
        lt.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add)


def test_reduce_leaf():
    bt = Leaf(2)
    res = LTree.init_from_bt(bt, 1).reduce(fun.max3)
    exp = bt.reduce(fun.max3)
    assert exp == res


def test_reduce_node():
    bt = Node(1, Leaf(2), Leaf(3))
    res = LTree.init_from_bt(bt, 1).reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    exp = bt.reduce(fun.max3)
    assert exp == res

# -------------------------- #


def test_uacc_empty():
    lt = LTree()
    with pytest.raises(AssertionError):
        lt.uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)


def test_uacc_illformed():
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg3 = Segment([(72, TAG_NODE), (92, TAG_LEAF), (42, TAG_LEAF)])
    lt = LTree([seg1, seg3])
    with pytest.raises(IllFormedError):
        lt.uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)


def test_uacc_leaf():
    m = 1
    bt = Leaf(1)
    res = LTree.init_from_bt(bt, m).uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)
    exp = LTree.init_from_bt(bt.uacc(fun.add), m)
    assert exp == res


def test_uacc_node():
    m = 1
    bt = Node(1, Leaf(2), Leaf(3))
    res = LTree.init_from_bt(bt, m).uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)
    exp = LTree.init_from_bt(bt.uacc(fun.add), m)
    assert exp == res


def test_uacc():
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg2 = Segment([(31, TAG_NODE), (47, TAG_LEAF), (32, TAG_LEAF)])
    seg3 = Segment([(72, TAG_NODE), (92, TAG_LEAF), (42, TAG_LEAF)])
    lt = LTree([seg1, seg2, seg3])
    res = lt.uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)

    seg1_exp = Segment([(13 + 31 + 47 + 32 + 72 + 92 + 42, TAG_CRITICAL)])
    seg2_exp = Segment([(31 + 47 + 32, TAG_NODE), (47, TAG_LEAF), (32, TAG_LEAF)])
    seg3_exp = Segment([(72 + 92 + 42, TAG_NODE), (92, TAG_LEAF), (42, TAG_LEAF)])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp])

    assert exp == res

# -------------------------- #


def test_dacc_empty():
    c = 0
    lt = LTree()
    with pytest.raises(AssertionError):
        lt.dacc(operator.add, operator.add, c, fun.idt, fun.idt, operator.add, operator.add)


def test_dacc():
    c = 0
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg2 = Segment([(31, TAG_NODE), (47, TAG_LEAF), (32, TAG_LEAF)])
    seg3 = Segment([(72, TAG_NODE), (92, TAG_LEAF), (42, TAG_LEAF)])
    lt = LTree([seg1, seg2, seg3])
    res = lt.dacc(operator.add, operator.add, c, fun.idt, fun.idt, operator.add, operator.add)
    seg1_exp = Segment([(0, TAG_CRITICAL)])
    seg2_exp = Segment([(13, TAG_NODE), (13 + 31, TAG_LEAF), (13 + 31, TAG_LEAF)])
    seg3_exp = Segment([(13, TAG_NODE), (13 + 72, TAG_LEAF), (13 + 72, TAG_LEAF)])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp])
    assert res == exp

def test_dacc_leaf():
    m = 1
    c = 0
    bt = Leaf(1)
    res = LTree.init_from_bt(bt, m).dacc(operator.add, operator.add, c, fun.idt, fun.idt, operator.add, operator.add)
    exp = LTree.init_from_bt(bt.dacc(operator.add, operator.add, c), m)
    assert exp == res


def test_dacc_node():
    m = 1
    c = 0
    bt = Node(1, Node(2, Leaf(3), Leaf(4)), Leaf(5))
    res = LTree.init_from_bt(bt, m).dacc(operator.add, operator.add, c, fun.idt, fun.idt, operator.add, operator.add)
    exp = LTree.init_from_bt(bt.dacc(operator.add, operator.add, c), m)
    assert exp == res

# -------------------------- #


def test_zip_leaf():
    m = 1
    bt1 = Leaf(1)
    bt2 = Leaf(2)
    res = LTree.init_from_bt(bt1, m).zip(LTree.init_from_bt(bt2, m))
    exp = LTree.init_from_bt(bt1.zip(bt2), m)
    assert exp == res


def test_zip_node():
    m = 1
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Node(4, Leaf(5), Leaf(6))
    res = LTree.init_from_bt(bt1, m).zip(LTree.init_from_bt(bt2, m))
    exp = LTree.init_from_bt(bt1.zip(bt2), m)
    assert exp == res


def test_zip_leaf_node():
    m = 1
    bt1 = Leaf(1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    with pytest.raises(AssertionError):
        LTree.init_from_bt(bt1, m).zip(LTree.init_from_bt(bt2, m))


def test_zip_node_leaf():
    m = 1
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Leaf(2)
    with pytest.raises(AssertionError):
        LTree.init_from_bt(bt1, m).zip(LTree.init_from_bt(bt2, m))

# -------------------------- #


def test_zipwith_leaf():
    m = 1
    bt1 = Leaf(1)
    bt2 = Leaf(2)
    res = LTree.init_from_bt(bt1, m).map2(fun.add, fun.add, LTree.init_from_bt(bt2, m))
    exp = LTree.init_from_bt(bt1.map2(fun.add, fun.add, bt2), m)
    assert exp == res


def test_zipwith_node():
    m = 1
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Node(4, Leaf(5), Leaf(6))
    res = LTree.init_from_bt(bt1, m).map2(fun.add, fun.add, LTree.init_from_bt(bt2, m))
    exp = LTree.init_from_bt(bt1.map2(fun.add, fun.add, bt2), m)
    assert exp == res


def test_zipwith_leaf_node():
    m = 1
    bt1 = Leaf(1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    with pytest.raises(AssertionError):
        LTree.init_from_bt(bt1, m).map2(fun.add, fun.add, LTree.init_from_bt(bt2, m))


def test_zipwith_node_leaf():
    m = 1
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Leaf(2)
    with pytest.raises(AssertionError):
        LTree.init_from_bt(bt1, m).map2(fun.add, fun.add, LTree.init_from_bt(bt2, m))
