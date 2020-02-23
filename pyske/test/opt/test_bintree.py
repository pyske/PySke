from pyske.core.tree.btree import Leaf, Node
from pyske.core.tree.ltree import LTree as DLTree
from pyske.core.tree.ptree import PTree as DPTree
from pyske.core.util import fun

from pyske.core.opt.bintree import LTree, PTree

# -------------------------- #

def test_ltree_constructor():
    m = 1
    bt = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
    exp = DLTree.from_bt(bt, m).to_bt()
    res = LTree.from_bt(bt, m).to_bt().run()
    assert res == exp


def test_ptree_constructor():
    m = 1
    bt = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
    exp = DPTree.from_bt(bt, m).to_bt()
    res = PTree.from_bt(bt, m).to_bt().run()
    assert res == exp


def test_ptree_constructor_seq():
    m = 1
    lt = DLTree.from_bt(Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2)), m)
    exp = DPTree.from_seq(lt).to_bt()
    res = PTree.from_seq(lt).to_bt().run()
    assert res == exp
# -------------------------- #


def test_ltree():
    m = 1
    bt1 = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
    bt2 = Node(6, Node(8, Leaf(4), Leaf(3)), Leaf(4))
    exp = DLTree.from_bt(bt1, m).map2(fun.add, fun.add, DLTree.from_bt(bt2, m))\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    res = LTree.from_bt(bt1, m).map2(fun.add, fun.add, LTree.from_bt(bt2, m))\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .map(lambda x: x + 1, lambda x: x - 1).to_bt()\
        .reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)\
        .run()
    assert res == exp


def test_ptree():
    m = 1
    bt1 = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
    bt2 = Node(6, Node(8, Leaf(4), Leaf(3)), Leaf(4))
    exp = DPTree.from_bt(bt1, m).map2(fun.add, fun.add, DPTree.from_bt(bt2, m))\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    res = PTree.from_bt(bt1, m).map2(fun.add, fun.add, PTree.from_bt(bt2, m))\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .map(lambda x: x + 1, lambda x: x - 1).to_bt()\
        .reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)\
        .run()
    assert res == exp

# -------------------------- #


def test_ltree_with_raw():
    m = 1
    bt1 = DLTree.from_bt(Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2)), m)
    bt2 = DLTree.from_bt(Node(6, Node(8, Leaf(4), Leaf(3)), Leaf(4)), m)
    exp = bt1.map2(fun.add, fun.add, bt2)\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    res = LTree.raw(bt1).map2(fun.add, fun.add, LTree.raw(bt2))\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .map(lambda x: x + 1, lambda x: x - 1).to_bt()\
        .reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)\
        .run()
    assert res == exp


def test_ptree_with_raw():
    m = 1
    bt1 = DPTree.from_bt(Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2)), m)
    bt2 = DPTree.from_bt(Node(6, Node(8, Leaf(4), Leaf(3)), Leaf(4)), m)
    exp = bt1.map2(fun.add, fun.add, bt2)\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)
    res = PTree.raw(bt1).map2(fun.add, fun.add, PTree.raw(bt2))\
        .map(lambda x: x + 1, lambda x: x - 1)\
        .map(lambda x: x + 1, lambda x: x - 1).to_bt()\
        .reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)\
        .run()
    assert res == exp