import pytest

from pyske.core.tree.btree import Leaf, Node
from pyske.core.runnable.tree.btree import BTree


# -------------------------- #

def test_is_leaf_true():
    bt = Leaf(1)
    res = BTree(bt).is_leaf().run()
    exp = bt.is_leaf()
    assert exp == res


def test_is_leaf_false():
    bt = Node(1, Leaf(1), Leaf(1))
    res = BTree(bt).is_leaf().run()
    exp = bt.is_leaf()
    assert exp == res

# -------------------------- #


def test_is_node_false():
    bt = Leaf(1)
    res = BTree(bt).is_node().run()
    exp = bt.is_node()
    assert exp == res


def test_is_node_true():
    bt = Node(1, Leaf(1), Leaf(1))
    res = BTree(bt).is_node().run()
    exp = bt.is_node()
    assert exp == res

# -------------------------- #


def test_map_leaf():
    bt = Leaf(1)
    kl = lambda x : x + 1
    kn = lambda x : x - 1
    res = BTree(bt).map(kl, kn).run()
    exp = bt.map(kl, kn)
    assert exp == res


def test_map_node():
    bt = Node(1, Leaf(2), Leaf(3))
    kl = lambda x: x + 1
    kn = lambda x: x - 1
    res = BTree(bt).map(kl, kn).run()
    exp = bt.map(kl, kn)
    assert exp == res


# -------------------------- #

def test_mapt_leaf():
    bt = Leaf(1)
    kl = lambda x: x + 1
    kn = lambda x, y, z: max(x, max(y.get_value(), z.get_value()))
    res = BTree(bt).mapt(kl, kn).run()
    exp = bt.mapt(kl, kn)
    assert exp == res


def test_mapt_node():
    bt = Node(1, Leaf(2), Leaf(3))
    kl = lambda x: x + 1
    kn = lambda x, y, z: max(x, max(y.get_value(), z.get_value()))
    res = BTree(bt).mapt(kl, kn).run()
    exp = bt.mapt(kl, kn)
    assert exp == res

# -------------------------- #


def test_reduce_leaf():
    bt = Leaf(2)
    k = lambda x, y, z: max(x, max(y, z))
    res = BTree(bt).reduce(k).run()
    exp = bt.reduce(k)
    assert exp == res


def test_reduce_node():
    bt = Node(1, Leaf(2), Leaf(3))
    k = lambda x, y, z: max(x, max(y, z))
    res = BTree(bt).reduce(k).run()
    exp = bt.reduce(k)
    assert exp == res

# -------------------------- #


def test_uacc_leaf():
    bt = Leaf(1)
    k = lambda x, y, z: x + y + z
    res = BTree(bt).uacc(k).run()
    exp = bt.uacc(k)
    assert exp == res


def test_uacc_node():
    bt = Node(1, Leaf(2), Leaf(3))
    k = lambda x, y, z: x + y + z
    res = BTree(bt).uacc(k).run()
    exp = bt.uacc(k)
    assert exp == res

# -------------------------- #


def test_dacc_leaf():
    c = 0
    bt = Leaf(1)
    gl = lambda x, y: x+y
    gr = lambda x, y: 0 if x-y < 0 else x-y
    res = BTree(bt).dacc(gl, gr, c).run()
    exp = bt.dacc(gl, gr, c)
    assert exp == res


def test_dacc_node():
    c = 0
    bt = Node(1, Node(2, Leaf(3), Leaf(4)), Leaf(5))
    gl = lambda x, y: x+y
    gr = lambda x, y: 0 if x-y < 0 else x-y
    res = BTree(bt).dacc(gl, gr, c).run()
    exp = bt.dacc(gl, gr, c)
    assert exp == res

# -------------------------- #


def test_zip_leaf():
    bt1 = Leaf(1)
    bt2 = Leaf(2)
    res = BTree(bt1).zip(BTree(bt2)).run()
    exp = bt1.zip(bt2)
    assert exp == res


def test_zip_node():
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Node(4, Leaf(5), Leaf(6))
    res = BTree(bt1).zip(BTree(bt2)).run()
    exp = bt1.zip(bt2)
    assert exp == res


def test_zip_leaf_node():
    bt1 = Leaf(1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    with pytest.raises(AssertionError):
        BTree(bt1).zip(BTree(bt2)).run()


def test_zip_node_leaf():
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Leaf(2)
    with pytest.raises(AssertionError):
        BTree(bt1).zip(BTree(bt2)).run()

# -------------------------- #


def test_zipwith_leaf():
    bt1 = Leaf(1)
    bt2 = Leaf(2)
    f = lambda x, y: x + y
    res = BTree(bt1).map2(f, BTree(bt2)).run()
    exp = bt1.map2(f, bt2)
    assert exp == res


def test_zipwith_node():
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Node(4, Leaf(5), Leaf(6))
    f = lambda x, y: x + y
    res = BTree(bt1).map2(f, BTree(bt2)).run()
    exp = bt1.map2(f, bt2)
    assert exp == res


def test_zipwith_leaf_node():
    bt1 = Leaf(1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    f = lambda x, y: x + y
    with pytest.raises(AssertionError):
        BTree(bt1).map2(f, BTree(bt2)).run()


def test_zipwith_node_leaf():
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Leaf(2)
    f = lambda x, y: x + y
    with pytest.raises(AssertionError):
        BTree(bt1).map2(f, BTree(bt2)).run()

# -------------------------- #


def test_getchl_leaf():
    c = 1
    bt = Leaf(3)
    res = BTree(bt).getchl(c).run()
    exp = bt.getchl(c)
    assert res == exp


def test_getchl_node_right():
    c = 1
    bt = Node(3, Leaf(2), Node(4, Leaf(2), Leaf(6)))
    res = BTree(bt).getchl(c).run()
    exp = bt.getchl(c)
    assert res == exp


def test_getchl_node_left():
    c = 1
    bt = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
    res = BTree(bt).getchl(c).run()
    exp = bt.getchl(c)
    assert res == exp

# -------------------------- #


def test_getchr_leaf():
    c = 1
    bt = Leaf(3)
    res = BTree(bt).getchr(c).run()
    exp = bt.getchr(c)
    assert res == exp


def test_getchr_node_right():
    c = 1
    bt = Node(3, Leaf(2), Node(4, Leaf(2), Leaf(6)))
    res = BTree(bt).getchr(c).run()
    exp = bt.getchr(c)
    assert res == exp


def test_getchr_node_left():
    c = 1
    bt = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
    res = BTree(bt).getchr(c).run()
    exp = bt.getchr(c)
    assert res == exp


# -------------------------- #


def test_composition_leaf():
    bt1 = Leaf(1)
    bt2 = Leaf(2)
    f = lambda x, y: x + y
    kl = lambda x: x + 1
    kn = lambda x: x - 1
    k = lambda x, y, z: x + y + z
    res = BTree(bt1).map(kl, kn).map2(f, BTree(bt2).uacc(k)).uacc(k).reduce(k).run()
    exp = bt1.map(kl, kn).map2(f, bt2.uacc(k)).uacc(k).reduce(k)
    assert exp == res


def test_composition_node():
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt2 = Node(4, Leaf(5), Leaf(6))
    f = lambda x, y: x + y
    kl = lambda x: x + 1
    kn = lambda x: x - 1
    k = lambda x, y, z: x + y + z
    res = BTree(bt1).map(kl, kn).map2(f, BTree(bt2).uacc(k)).uacc(k).reduce(k).run()
    exp = bt1.map(kl, kn).map2(f, bt2.uacc(k)).uacc(k).reduce(k)
    assert exp == res
