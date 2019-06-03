import pytest

from pyske.core.tree.btree import Leaf, Node
from pyske.core.runnable.tree.ebtree import EBTree


# -------------------------- #

def test_is_leaf_true():
    bt = Leaf(1)
    bt_run = EBTree(bt)
    bt_run.is_leaf()
    res = bt_run.run()
    exp = bt.is_leaf()
    assert exp == res


def test_is_leaf_false():
    bt = Node(1, Leaf(1), Leaf(1))
    bt_run = EBTree(bt)
    bt_run.is_leaf()
    res = bt_run.run()
    exp = bt.is_leaf()
    assert exp == res

# -------------------------- #

def test_is_node_false():
    bt = Leaf(1)
    bt_run = EBTree(bt)
    bt_run.is_node()
    res = bt_run.run()
    exp = bt.is_node()
    assert exp == res


def test_is_node_true():
    bt = Node(1, Leaf(1), Leaf(1))
    bt_run = EBTree(bt)
    bt_run.is_node()
    res = bt_run.run()
    exp = bt.is_node()
    assert exp == res

# -------------------------- #

def test_map_leaf():
    bt = Leaf(1)
    bt_run = EBTree(bt)
    kl = lambda x : x + 1
    kn = lambda x : x - 1
    bt_run.map(kl, kn)
    res = bt_run.run()
    exp = bt.map(kl, kn)
    assert exp == res


def test_map_node():
    bt = Node(1, Leaf(2), Leaf(3))
    bt_run = EBTree(bt)
    kl = lambda x : x + 1
    kn = lambda x : x - 1
    bt_run.map(kl, kn)
    res = bt_run.run()
    exp = bt.map(kl, kn)
    assert exp == res


# -------------------------- #

def test_mapt_leaf():
    bt = Leaf(1)
    bt_run = EBTree(bt)
    kl = lambda x : x + 1
    kn = lambda x,y,z : max(x,max(y.get_value(),z.get_value()))
    bt_run.mapt(kl, kn)
    res = bt_run.run()
    exp = bt.mapt(kl, kn)
    assert exp == res


def test_mapt_node():
    bt = Node(1, Leaf(2), Leaf(3))
    bt_run = EBTree(bt)
    kl = lambda x : x + 1
    kn = lambda x,y,z : max(x,max(y.get_value(),z.get_value()))
    bt_run.mapt(kl, kn)
    res = bt_run.run()
    exp = bt.mapt(kl, kn)
    assert exp == res

# -------------------------- #

def test_reduce_leaf():
    bt = Leaf(2)
    bt_run = EBTree(bt)
    k = lambda x,y,z : max(x,max(y,z))
    bt_run.reduce(k)
    res = bt_run.run()
    exp = bt.reduce(k)
    assert exp == res


def test_reduce_node():
    bt = Node(1, Leaf(2), Leaf(3))
    bt_run = EBTree(bt)
    k = lambda x,y,z : max(x,max(y,z))
    bt_run.reduce(k)
    res = bt_run.run()
    exp = bt.reduce(k)
    assert exp == res

# -------------------------- #

def test_uacc_leaf():
    bt = Leaf(1)
    bt_run = EBTree(bt)
    k = lambda x,y,z : x + y + z
    bt_run.uacc(k)
    res = bt_run.run()
    exp = bt.uacc(k)
    assert exp == res


def test_uacc_node():
    bt = Node(1, Leaf(2), Leaf(3))
    bt_run = EBTree(bt)
    k = lambda x,y,z : x + y + z
    bt_run.uacc(k)
    res = bt_run.run()
    exp = bt.uacc(k)
    assert exp == res

# -------------------------- #

def test_dacc_leaf():
    c = 0
    bt = Leaf(1)
    bt_run = EBTree(bt)
    gl = lambda x, y: x+y
    gr = lambda x, y: 0 if x-y < 0 else x-y
    bt_run.dacc(gl, gr, c)
    res = bt_run.run()
    exp = bt.dacc(gl, gr, c)
    assert exp == res


def test_dacc_node():
    c = 0
    bt = Node(1, Node(2, Leaf(3), Leaf(4)), Leaf(5))
    bt_run = EBTree(bt)
    gl = lambda x, y: x+y
    gr = lambda x, y: 0 if x-y < 0 else x-y
    bt_run.dacc(gl, gr, c)
    res = bt_run.run()
    exp = bt.dacc(gl, gr, c)
    assert exp == res

# -------------------------- #

def test_zip_leaf():
    bt1 = Leaf(1)
    bt1_run = EBTree(bt1)
    bt2 = Leaf(2)
    bt2_run = EBTree(bt2)
    bt1_run.zip(bt2_run)
    res = bt1_run.run()
    exp = bt1.zip(bt2)
    assert exp == res


def test_zip_node():
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt1_run = EBTree(bt1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    bt2_run = EBTree(bt2)
    bt1_run.zip(bt2_run)
    res = bt1_run.run()
    exp = bt1.zip(bt2)
    assert exp == res


def test_zip_leaf_node():
    bt1 = Leaf(1)
    bt1_run = EBTree(bt1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    bt2_run = EBTree(bt2)
    bt1_run.zip(bt2_run)
    with pytest.raises(AssertionError):
        bt1_run.run()


def test_zip_node_leaf():
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt1_run = EBTree(bt1)
    bt2 = Leaf(2)
    bt2_run = EBTree(bt2)
    bt1_run.zip(bt2_run)
    with pytest.raises(AssertionError):
        bt1_run.run()

# -------------------------- #

def test_zipwith_leaf():
    bt1 = Leaf(1)
    bt1_run = EBTree(bt1)
    bt2 = Leaf(2)
    bt2_run = EBTree(bt2)
    f = lambda x,y : x + y
    bt1_run.map2(f, bt2_run)
    res = bt1_run.run()
    exp = bt1.map2(f, bt2)
    assert exp == res


def test_zipwith_node():
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt1_run = EBTree(bt1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    bt2_run = EBTree(bt2)
    f = lambda x,y : x + y
    bt1_run.map2(f, bt2_run)
    res = bt1_run.run()
    exp = bt1.map2(f, bt2)
    assert exp == res


def test_zipwith_leaf_node():
    bt1 = Leaf(1)
    bt1_run = EBTree(bt1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    bt2_run = EBTree(bt2)
    f = lambda x,y : x + y
    bt1_run.map2(f, bt2_run)
    with pytest.raises(AssertionError):
        bt1_run.run()


def test_zipwith_node_leaf():
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt1_run = EBTree(bt1)
    bt2 = Leaf(2)
    bt2_run = EBTree(bt2)
    f = lambda x,y : x + y
    bt1_run.map2(f, bt2_run)
    with pytest.raises(AssertionError):
        bt1_run.run()

# -------------------------- #

def test_getchl_leaf():
    c = 1
    bt = Leaf(3)
    bt_run = EBTree(bt)
    bt_run.getchl(c)
    res = bt_run.run()
    exp = bt.getchl(c)
    assert res == exp


def test_getchl_node_right():
    c = 1
    bt = Node(3, Leaf(2), Node(4, Leaf(2), Leaf(6)))
    bt_run = EBTree(bt)
    bt_run.getchl(c)
    res = bt_run.run()
    exp = bt.getchl(c)
    assert res == exp


def test_getchl_node_left():
    c = 1
    bt = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
    bt_run = EBTree(bt)
    bt_run.getchl(c)
    res = bt_run.run()
    exp = bt.getchl(c)
    assert res == exp

# -------------------------- #

def test_getchr_leaf():
    c = 1
    bt = Leaf(3)
    bt_run = EBTree(bt)
    bt_run.getchr(c)
    res = bt_run.run()
    exp = bt.getchr(c)
    assert res == exp


def test_getchr_node_right():
    c = 1
    bt = Node(3, Leaf(2), Node(4, Leaf(2), Leaf(6)))
    bt_run = EBTree(bt)
    bt_run.getchr(c)
    res = bt_run.run()
    exp = bt.getchr(c)
    assert res == exp


def test_getchr_node_left():
    c = 1
    bt = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
    bt_run = EBTree(bt)
    bt_run.getchr(c)
    res = bt_run.run()
    exp = bt.getchr(c)
    assert res == exp


# -------------------------- #


def test_composition_leaf():
    bt1 = Leaf(1)
    bt1_run = EBTree(bt1)
    bt2 = Leaf(2)
    bt2_run = EBTree(bt2)
    f = lambda x, y: x + y
    kl = lambda x: x + 1
    kn = lambda x: x - 1
    k = lambda x, y, z: x + y + z
    bt1_run.map(kl, kn)
    bt2_run.uacc(k)
    bt1_run.map2(f, bt2_run)
    bt1_run.uacc(k)
    bt1_run.reduce(k)
    res = bt1_run.run()
    exp = bt1.map(kl, kn).map2(f, bt2.uacc(k)).uacc(k).reduce(k)
    assert exp == res

def test_composition_node():
    bt1 = Node(1, Leaf(2), Leaf(3))
    bt1_run = EBTree(bt1)
    bt2 = Node(4, Leaf(5), Leaf(6))
    bt2_run = EBTree(bt2)
    f = lambda x, y: x + y
    kl = lambda x: x + 1
    kn = lambda x: x - 1
    k = lambda x, y, z: x + y + z
    bt1_run.map(kl, kn)
    bt2_run.uacc(k)
    bt1_run.map2(f, bt2_run)
    bt1_run.uacc(k)
    bt1_run.reduce(k)
    res = bt1_run.run()
    exp = bt1.map(kl, kn).map2(f, bt2.uacc(k)).uacc(k).reduce(k)
    assert exp == res
