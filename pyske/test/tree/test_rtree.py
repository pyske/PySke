import pytest
import operator
from pyske.core.list.slist import SList
from pyske.core.support.errors import ConstructorError
from pyske.core.tree.btree import Node, Leaf
from pyske.core.tree.rtree import RNode


# -------------------------- #

def test_b2r_leaf_none():
    bt = Leaf(None)
    with pytest.raises(ConstructorError):
        RNode(bt)


def test_b2r_leaf():
    bt = Leaf(1)
    res = RNode(bt)
    exp = RNode(1)
    assert res == exp


def test_b2r_node_from_rt():
    bt = Node(1,
              Node(2,
                   Leaf(None),
                   Node(3,
                        Node(5,
                             Leaf(None),
                             Node(6,
                                  Leaf(None),
                                  Leaf(None)
                                  )
                             ),
                        Node(4,
                             Leaf(None),
                             Leaf(None)
                             )
                        )
                   ),
              Leaf(None)
              )
    rn5 = RNode(5)
    rn6 = RNode(6)
    rn3 = RNode(3, SList([rn5, rn6]))
    rn2 = RNode(2)
    rn4 = RNode(4)
    exp = RNode(1, SList([rn2, rn3, rn4]))
    res = RNode(bt)

    assert res == exp


# -------------------------- #

def test_r2b_1():
    ch = SList()
    ch.append(RNode(2))
    ch.append(RNode(3))
    rn = RNode(1, ch)
    res = rn.r2b()
    exp = Node(1, Node(2, Leaf(None), Node(3, Leaf(None), Leaf(None))), Leaf(None))
    assert res == exp


def test_r2b_2():
    rn5 = RNode(5)
    rn6 = RNode(6)
    rn3 = RNode(3, SList([rn5, rn6]))
    rn2 = RNode(2)
    rn4 = RNode(4)
    rn1 = RNode(1, SList([rn2, rn3, rn4]))
    res = rn1.r2b()
    exp = \
        Node(1,
             Node(2,
                  Leaf(None),
                  Node(3,
                       Node(5,
                            Leaf(None),
                            Node(6,
                                 Leaf(None),
                                 Leaf(None)
                                 )
                            ),
                       Node(4,
                            Leaf(None),
                            Leaf(None)
                            )
                       )
                  ),
             Leaf(None)
             )
    assert res == exp


def test_map():
    rt = RNode(15, [RNode(24),
                    RNode(32, [RNode(56),
                               RNode(63)]),
                    RNode(41)])
    res = rt.map(str)
    exp = RNode("15", [RNode("24"),
                       RNode("32", [RNode("56"),
                                    RNode("63")]),
                       RNode("41")])
    assert res == exp


def test_reduce():
    rt = RNode(15, [RNode(24),
                    RNode(32, [RNode(56),
                               RNode(63)]),
                    RNode(41)])
    res = rt.reduce(operator.add, operator.mul)
    exp = 3503055
    assert res == exp


def test_uacc():
    rt = RNode(15, [RNode(24),
                    RNode(32, [RNode(56),
                               RNode(63)]),
                    RNode(41)])
    res = rt.uacc(operator.add, operator.mul)
    exp = RNode(3503055, [RNode(24),
                          RNode(3560, [RNode(56),
                                       RNode(63)]),
                          RNode(41)])
    assert res == exp


def test_dacc():
    rt = RNode(15, [RNode(24),
                    RNode(32, [RNode(56),
                               RNode(63)]),
                    RNode(41)])
    res = rt.dacc(operator.add, 0)
    exp = RNode(0, [RNode(15),
                    RNode(15, [RNode(47),
                               RNode(47)]),
                    RNode(15)])
    assert res == exp


def test_lacc():
    rt = RNode(15, [RNode(24),
                    RNode(32, [RNode(56),
                               RNode(63)]),
                    RNode(41)])
    res = rt.lacc(operator.add, 0)
    exp = RNode(0, [RNode(73),
                    RNode(41, [RNode(63),
                               RNode(0)]),
                    RNode(0)])
    assert res == exp


def test_racc():
    rt = RNode(15, [RNode(24),
                    RNode(32, [RNode(56),
                               RNode(63)]),
                    RNode(41)])
    res = rt.racc(operator.add, 0)
    exp = RNode(0, [RNode(0),
                    RNode(24,
                          [RNode(0),
                           RNode(56)]),
                    RNode(56)])
    assert res == exp
