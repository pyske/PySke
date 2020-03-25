from pyske.core.support.generate import *
from pyske.core.support.errors import IllFormedError
from pyske.core.tree.btree import Leaf, Node
from pyske.core.tree.ltree import LTree
from pyske.core.tree.segment import Segment
from pyske.core.tree.tag import TAG_LEAF, TAG_NODE, TAG_CRITICAL
from pyske.core.util import fun
from random import randint
from pyske.examples.tree.tree_functions import *

import operator
import pytest
# -------------------------- #


def test_map_empty():
    lt = LTree()
    with pytest.raises(AssertionError):
        lt.map(fun.idt, fun.idt)


def test_map_leaf():
    bt = Leaf(1)
    res = LTree.from_bt(bt, 1).map(lambda x: x + 1, lambda x: x - 1)
    exp = LTree.from_bt(Leaf(2), 1)
    assert exp == res


def test_map_node():
    bt = Node(1, Leaf(2), Leaf(3))
    res = LTree.from_bt(bt, 1).map(fun.incr, fun.decr)
    exp = LTree.from_bt(Node(0, Leaf(3), Leaf(4)), 1)
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
    res = LTree.from_bt(bt, 1).reduce(fun.max3)
    exp = bt.reduce(fun.max3)
    assert exp == res


def test_reduce_node():
    bt = Node(1, Leaf(2), Leaf(3))
    res = LTree.from_bt(bt, 1).reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
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
    res = LTree.from_bt(bt, m).uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)
    exp = LTree.from_bt(bt.uacc(fun.add), m)
    assert exp == res


def test_uacc_node():
    m = 1
    bt = Node(1, Leaf(2), Leaf(3))
    res = LTree.from_bt(bt, m).uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)
    exp = LTree.from_bt(bt.uacc(fun.add), m)
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
    res = LTree.from_bt(bt, m).dacc(operator.add, operator.add, c, fun.idt, fun.idt, operator.add, operator.add)
    exp = LTree.from_bt(bt.dacc(operator.add, operator.add, c), m)
    assert exp == res


def test_dacc_node():
    m = 1
    c = 0
    bt = Node(1, Node(2, Leaf(3), Leaf(4)), Leaf(5))
    res = LTree.from_bt(bt, m).dacc(operator.add, operator.add, c, fun.idt, fun.idt, operator.add, operator.add)
    exp = LTree.from_bt(bt.dacc(operator.add, operator.add, c), m)
    assert exp == res

# -------------------------- #


def test_zip_leaf():
    m = 1
    bt1 = Leaf(1)
    bt2 = Leaf(2)
    res = LTree.from_bt(bt1, m).zip(LTree.from_bt(bt2, m))
    exp = LTree.from_bt(bt1.zip(bt2), m)
    assert exp == res


def test_zip_node():
    m = 1
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Node(4, Leaf(5), Leaf(6))
    res = LTree.from_bt(bt1, m).zip(LTree.from_bt(bt2, m))
    exp = LTree.from_bt(bt1.zip(bt2), m)
    assert exp == res


def test_zip_leaf_node():
    m = 1
    bt1 = Leaf(1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    with pytest.raises(AssertionError):
        LTree.from_bt(bt1, m).zip(LTree.from_bt(bt2, m))


def test_zip_node_leaf():
    m = 1
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Leaf(2)
    with pytest.raises(AssertionError):
        LTree.from_bt(bt1, m).zip(LTree.from_bt(bt2, m))

# -------------------------- #


def test_zipwith_leaf():
    m = 1
    bt1 = Leaf(1)
    bt2 = Leaf(2)
    res = LTree.from_bt(bt1, m).map2(fun.add, fun.add, LTree.from_bt(bt2, m))
    exp = LTree.from_bt(bt1.map2(fun.add, fun.add, bt2), m)
    assert exp == res


def test_zipwith_node():
    m = 1
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Node(4, Leaf(5), Leaf(6))
    res = LTree.from_bt(bt1, m).map2(fun.add, fun.add, LTree.from_bt(bt2, m))
    exp = LTree.from_bt(bt1.map2(fun.add, fun.add, bt2), m)
    assert exp == res


def test_zipwith_leaf_node():
    m = 1
    bt1 = Leaf(1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    with pytest.raises(AssertionError):
        LTree.from_bt(bt1, m).map2(fun.add, fun.add, LTree.from_bt(bt2, m))


def test_zipwith_node_leaf():
    m = 1
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Leaf(2)
    with pytest.raises(AssertionError):
        LTree.from_bt(bt1, m).map2(fun.add, fun.add, LTree.from_bt(bt2, m))

# -------------------------- #


def test_prefix():
    m = 1
    bt = balanced_btree(lambda: randint(0, 10), 20)
    lt = LTree.from_bt(bt, m)
    res = prefix(lt).to_bt()
    exp = prefix(bt)
    assert exp == res


def test_depth():
    m = 1
    bt = balanced_btree(lambda: randint(0, 10), 20)
    lt = LTree.from_bt(bt, m)
    res = depth(lt).to_bt()
    exp = depth(bt)
    assert exp == res


def test_ancestors():
    m = 1
    bt = balanced_btree(lambda: randint(0, 10), 20)
    lt = LTree.from_bt(bt, m)
    res = ancestors(lt).to_bt()
    exp = ancestors(bt)
    assert exp == res


def test_l_ancestors():
    m = 1
    bt = balanced_btree(lambda: randint(0, 10), 20)
    lt = LTree.from_bt(bt, m)
    res = l_ancestors(lt).to_bt()
    exp = l_ancestors(bt)
    assert exp == res

# -------------------------- #

def test_map_reduce_leaf():
    bt = Leaf(1)
    m = 1
    lt = LTree.from_bt(bt, m)
    exp = lt.map(lambda x: x + 1, lambda x: x - 1).reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    res = lt.map_reduce(lambda x: x + 1, lambda x: x - 1, fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    assert exp == res


def test_map_reduce_node():
    bt = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
    m = 1
    lt = LTree.from_bt(bt, m)
    exp = lt.map(lambda x: x + 1, lambda x: x - 1).reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    res = lt.map_reduce(lambda x: x + 1, lambda x: x - 1, fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    assert exp == res

# -------------------------- #


def test_zip_reduce_leaf():
    m = 1
    bt1 = Leaf(1)
    bt2 = Leaf(2)
    lt1 = LTree.from_bt(bt1, m)
    lt2 = LTree.from_bt(bt2, m)
    exp = lt1.zip(lt2).reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    res = lt1.zip_reduce(lt2, fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    assert exp == res


def test_zip_reduce_node():
    m = 1
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Node(4, Leaf(5), Leaf(6))
    lt1 = LTree.from_bt(bt1, m)
    lt2 = LTree.from_bt(bt2, m)
    exp = lt1.zip(lt2).reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    res = lt1.zip_reduce(lt2, fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    assert exp == res

# -------------------------- #


def test_map2_reduce_leaf():
    m = 1
    bt1 = Leaf(1)
    bt2 = Leaf(2)
    lt1 = LTree.from_bt(bt1, m)
    lt2 = LTree.from_bt(bt2, m)
    exp = lt1.map2(fun.add, fun.add, lt2).reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    res = lt1.map2_reduce(fun.add, fun.add, lt2, fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    assert exp == res


def test_map2_reduce_node():
    m = 1
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Node(4, Leaf(5), Leaf(6))
    lt1 = LTree.from_bt(bt1, m)
    lt2 = LTree.from_bt(bt2, m)
    exp = lt1.map2(fun.add, fun.add, lt2).reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    res = lt1.map2_reduce(fun.add, fun.add, lt2, fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    assert exp == res