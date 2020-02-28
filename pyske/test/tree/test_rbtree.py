from pyske.core import SList
from pyske.core.tree.rbtree import RLeaf, RNode
from pyske.core.tree.rtree import RTree


def test_map():
    rt = RTree('1', SList([RTree('2'),
                           RTree('3', SList([RTree('5'), RTree('6')])),
                           RTree('4')]))
    res = RNode.from_rt(rt).map(lambda x: int(x))
    exp = RNode.from_rt(rt.map(lambda x: int(x)))
    assert res == exp


def test_map2():
    rt1 = RTree('A', SList([RTree('B'),
                           RTree('C', SList([RTree('E'), RTree('F')])),
                           RTree('D')]))
    rt2 = RTree('1', SList([RTree('2'),
                           RTree('3', SList([RTree('5'), RTree('6')])),
                           RTree('4')]))
    res = RNode.from_rt(rt1).map2(lambda x, y: (x, y), RNode.from_rt(rt2))
    exp = RNode.from_rt(rt1.map2(lambda x, y: (x, y), rt2))
    assert res == exp


def test_zip():
    rt1 = RTree('A', SList([RTree('B'),
                           RTree('C', SList([RTree('E'), RTree('F')])),
                           RTree('D')]))
    rt2 = RTree('1', SList([RTree('2'),
                           RTree('3', SList([RTree('5'), RTree('6')])),
                           RTree('4')]))
    res = RNode.from_rt(rt1).zip(RNode.from_rt(rt2))
    exp = RNode.from_rt(rt1.zip(rt2))
    assert res == exp


def test_eq():
    rt1 = RTree('A', SList([RTree('B'),
                           RTree('C', SList([RTree('E'), RTree('F')])),
                           RTree('D')]))
    rt2 = RTree('1', SList([RTree('2'),
                           RTree('3', SList([RTree('5'), RTree('6')])),
                           RTree('4')]))
    res = RNode.from_rt(rt1).zip(RNode.from_rt(rt2)).map(lambda x: x[0] + x[1])
    exp = RNode.from_rt(rt1.zip(rt2).map(lambda x: x[0] + x[1]))
    assert res == exp
