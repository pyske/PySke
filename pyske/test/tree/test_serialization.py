from pyske.core.tree.btree import Node, Leaf
from pyske.core.tree.ltree import LTree, Segment, TAG_LEAF, TAG_CRITICAL, TAG_NODE


# -------------------------- #

def test_serialization_1_4():
    # btree4
    bt = Node(1, Node(2, Node(4, Leaf(6), Leaf(7)), Node(5, Leaf(8), Leaf(9))), Leaf(3))
    m = 4
    res = LTree.init_from_bt(bt, m)
    seg1 = Segment([(1, TAG_CRITICAL)])
    seg2 = Segment([(2, TAG_CRITICAL)])
    seg3 = Segment([(4, TAG_NODE), (6, TAG_LEAF), (7, TAG_LEAF)])
    seg4 = Segment([(5, TAG_NODE), (8, TAG_LEAF), (9, TAG_LEAF)])
    seg5 = Segment([(3, TAG_LEAF)])
    exp = LTree([seg1, seg2, seg3, seg4, seg5])
    assert res == exp


def test_serialization_1_3():
    # btree4
    bt = Node(1, Node(2, Node(4, Leaf(6), Leaf(7)), Node(5, Leaf(8), Leaf(9))), Leaf(3))
    m = 3
    res = LTree.init_from_bt(bt, m)
    seg1 = Segment([(1, TAG_NODE), (2, TAG_CRITICAL), (3, TAG_LEAF)])
    seg2 = Segment([(4, TAG_NODE), (6, TAG_LEAF), (7, TAG_LEAF)])
    seg3 = Segment([(5, TAG_NODE), (8, TAG_LEAF), (9, TAG_LEAF)])
    exp = LTree([seg1, seg2, seg3])
    assert res == exp


def test_serialization_1_2():
    # btree4
    bt = Node(1, Node(2, Node(4, Leaf(6), Leaf(7)), Node(5, Leaf(8), Leaf(9))), Leaf(3))
    m = 2
    res = LTree.init_from_bt(bt, m)
    seg1 = Segment([(1, TAG_CRITICAL)])
    seg2 = Segment([(2, TAG_CRITICAL)])
    seg3 = Segment([(4, TAG_CRITICAL)])
    seg4 = Segment([(6, TAG_LEAF)])
    seg5 = Segment([(7, TAG_LEAF)])
    seg6 = Segment([(5, TAG_CRITICAL)])
    seg7 = Segment([(8, TAG_LEAF)])
    seg8 = Segment([(9, TAG_LEAF)])
    seg9 = Segment([(3, TAG_LEAF)])
    exp = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9])
    assert res == exp


def test_serialization_1_1():
    # btree4
    bt = Node(1, Node(2, Node(4, Leaf(6), Leaf(7)), Node(5, Leaf(8), Leaf(9))), Leaf(3))
    m = 1
    res = LTree.init_from_bt(bt, m)
    seg1 = Segment([(1, TAG_CRITICAL)])
    seg2 = Segment([(2, TAG_CRITICAL)])
    seg3 = Segment([(4, TAG_CRITICAL)])
    seg4 = Segment([(6, TAG_LEAF)])
    seg5 = Segment([(7, TAG_LEAF)])
    seg6 = Segment([(5, TAG_CRITICAL)])
    seg7 = Segment([(8, TAG_LEAF)])
    seg8 = Segment([(9, TAG_LEAF)])
    seg9 = Segment([(3, TAG_LEAF)])
    exp = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9])
    assert res == exp


def test_serialization_2_5():
    # btree5
    bt = Node(13, Node(3, Leaf(1), Leaf(1)),
              Node(9, Node(7, Node(3, Leaf(1), Leaf(1)), Node(3, Leaf(1), Leaf(1))), Leaf(1)))
    m = 5
    res = LTree.init_from_bt(bt, m)
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg2 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg3 = Segment([(9, TAG_NODE), (7, TAG_CRITICAL), (1, TAG_LEAF)])
    seg4 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg5 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    exp = LTree([seg1, seg2, seg3, seg4, seg5])
    assert res == exp


def test_serialization_2_4():
    # btree5
    bt = Node(13, Node(3, Leaf(1), Leaf(1)),
              Node(9, Node(7, Node(3, Leaf(1), Leaf(1)), Node(3, Leaf(1), Leaf(1))), Leaf(1)))
    m = 4
    res = LTree.init_from_bt(bt, m)
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg2 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg3 = Segment([(9, TAG_CRITICAL)])
    seg4 = Segment([(7, TAG_CRITICAL)])
    seg5 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg6 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg7 = Segment([(1, TAG_LEAF)])
    exp = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7])
    assert res == exp


def test_serialization_2_3():
    # btree5
    bt = Node(13, Node(3, Leaf(1), Leaf(1)),
              Node(9, Node(7, Node(3, Leaf(1), Leaf(1)), Node(3, Leaf(1), Leaf(1))), Leaf(1)))
    m = 3
    res = LTree.init_from_bt(bt, m)
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg2 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg3 = Segment([(9, TAG_NODE), (7, TAG_CRITICAL), (1, TAG_LEAF)])
    seg4 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg5 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    exp = LTree([seg1, seg2, seg3, seg4, seg5])
    assert res == exp


def test_serialization_2_2():
    # btree5
    bt = Node(13, Node(3, Leaf(1), Leaf(1)),
              Node(9, Node(7, Node(3, Leaf(1), Leaf(1)), Node(3, Leaf(1), Leaf(1))), Leaf(1)))
    m = 2
    res = LTree.init_from_bt(bt, m)
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg2 = Segment([(3, TAG_CRITICAL)])
    seg3 = Segment([(1, TAG_LEAF)])
    seg4 = Segment([(1, TAG_LEAF)])
    seg5 = Segment([(9, TAG_CRITICAL)])
    seg6 = Segment([(7, TAG_CRITICAL)])
    seg7 = Segment([(3, TAG_CRITICAL)])
    seg8 = Segment([(1, TAG_LEAF)])
    seg9 = Segment([(1, TAG_LEAF)])
    seg10 = Segment([(3, TAG_CRITICAL)])
    seg11 = Segment([(1, TAG_LEAF)])
    seg12 = Segment([(1, TAG_LEAF)])
    seg13 = Segment([(1, TAG_LEAF)])
    exp = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9, seg10, seg11, seg12, seg13])
    assert res == exp


# -------------------------- #

def test_deserialization_1_4():
    # btree4
    seg1 = Segment([(1, TAG_CRITICAL)])
    seg2 = Segment([(2, TAG_CRITICAL)])
    seg3 = Segment([(4, TAG_NODE), (6, TAG_LEAF), (7, TAG_LEAF)])
    seg4 = Segment([(5, TAG_NODE), (8, TAG_LEAF), (9, TAG_LEAF)])
    seg5 = Segment([(3, TAG_LEAF)])
    lt = LTree([seg1, seg2, seg3, seg4, seg5])
    res = lt.deserialization()
    exp = Node(1, Node(2, Node(4, Leaf(6), Leaf(7)), Node(5, Leaf(8), Leaf(9))), Leaf(3))
    assert res == exp


def test_deserialization_1_3():
    # btree4
    exp = Node(1, Node(2, Node(4, Leaf(6), Leaf(7)), Node(5, Leaf(8), Leaf(9))), Leaf(3))
    seg1 = Segment([(1, TAG_NODE), (2, TAG_CRITICAL), (3, TAG_LEAF)])
    seg2 = Segment([(4, TAG_NODE), (6, TAG_LEAF), (7, TAG_LEAF)])
    seg3 = Segment([(5, TAG_NODE), (8, TAG_LEAF), (9, TAG_LEAF)])
    lt = LTree([seg1, seg2, seg3])
    res = lt.deserialization()
    assert res == exp


def test_deserialization_1_2():
    # btree4
    exp = Node(1, Node(2, Node(4, Leaf(6), Leaf(7)), Node(5, Leaf(8), Leaf(9))), Leaf(3))
    seg1 = Segment([(1, TAG_CRITICAL)])
    seg2 = Segment([(2, TAG_CRITICAL)])
    seg3 = Segment([(4, TAG_CRITICAL)])
    seg4 = Segment([(6, TAG_LEAF)])
    seg5 = Segment([(7, TAG_LEAF)])
    seg6 = Segment([(5, TAG_CRITICAL)])
    seg7 = Segment([(8, TAG_LEAF)])
    seg8 = Segment([(9, TAG_LEAF)])
    seg9 = Segment([(3, TAG_LEAF)])
    lt = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9])
    res = lt.deserialization()
    assert res == exp


def test_deserialization_1_1():
    # btree4
    exp = Node(1, Node(2, Node(4, Leaf(6), Leaf(7)), Node(5, Leaf(8), Leaf(9))), Leaf(3))
    seg1 = Segment([(1, TAG_CRITICAL)])
    seg2 = Segment([(2, TAG_CRITICAL)])
    seg3 = Segment([(4, TAG_CRITICAL)])
    seg4 = Segment([(6, TAG_LEAF)])
    seg5 = Segment([(7, TAG_LEAF)])
    seg6 = Segment([(5, TAG_CRITICAL)])
    seg7 = Segment([(8, TAG_LEAF)])
    seg8 = Segment([(9, TAG_LEAF)])
    seg9 = Segment([(3, TAG_LEAF)])
    lt = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9])
    res = lt.deserialization()
    assert res == exp


def test_deserialization_2_5():
    # btree5
    exp = Node(13, Node(3, Leaf(1), Leaf(1)),
               Node(9, Node(7, Node(3, Leaf(1), Leaf(1)), Node(3, Leaf(1), Leaf(1))), Leaf(1)))
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg2 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg3 = Segment([(9, TAG_NODE), (7, TAG_CRITICAL), (1, TAG_LEAF)])
    seg4 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg5 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    lt = LTree([seg1, seg2, seg3, seg4, seg5])
    res = lt.deserialization()
    assert res == exp


def test_deserialization_2_4():
    # btree5
    exp = Node(13, Node(3, Leaf(1), Leaf(1)),
               Node(9, Node(7, Node(3, Leaf(1), Leaf(1)), Node(3, Leaf(1), Leaf(1))), Leaf(1)))
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg2 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg3 = Segment([(9, TAG_CRITICAL)])
    seg4 = Segment([(7, TAG_CRITICAL)])
    seg5 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg6 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg7 = Segment([(1, TAG_LEAF)])
    lt = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7])
    res = lt.deserialization()
    assert res == exp


def test_deserialization_2_3():
    # btree5
    exp = Node(13, Node(3, Leaf(1), Leaf(1)),
               Node(9, Node(7, Node(3, Leaf(1), Leaf(1)), Node(3, Leaf(1), Leaf(1))), Leaf(1)))
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg2 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg3 = Segment([(9, TAG_NODE), (7, TAG_CRITICAL), (1, TAG_LEAF)])
    seg4 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    seg5 = Segment([(3, TAG_NODE), (1, TAG_LEAF), (1, TAG_LEAF)])
    lt = LTree([seg1, seg2, seg3, seg4, seg5])
    res = lt.deserialization()
    assert res == exp


def test_deserialization_2_2():
    # btree5
    exp = Node(13, Node(3, Leaf(1), Leaf(1)),
               Node(9, Node(7, Node(3, Leaf(1), Leaf(1)), Node(3, Leaf(1), Leaf(1))), Leaf(1)))
    seg1 = Segment([(13, TAG_CRITICAL)])
    seg2 = Segment([(3, TAG_CRITICAL)])
    seg3 = Segment([(1, TAG_LEAF)])
    seg4 = Segment([(1, TAG_LEAF)])
    seg5 = Segment([(9, TAG_CRITICAL)])
    seg6 = Segment([(7, TAG_CRITICAL)])
    seg7 = Segment([(3, TAG_CRITICAL)])
    seg8 = Segment([(1, TAG_LEAF)])
    seg9 = Segment([(1, TAG_LEAF)])
    seg10 = Segment([(3, TAG_CRITICAL)])
    seg11 = Segment([(1, TAG_LEAF)])
    seg12 = Segment([(1, TAG_LEAF)])
    seg13 = Segment([(1, TAG_LEAF)])
    lt = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9, seg10, seg11, seg12, seg13])
    res = lt.deserialization()
    assert res == exp
