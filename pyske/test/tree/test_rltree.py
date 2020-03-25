from pyske.core import SList
from pyske.core.tree.rltree import RLTree
from pyske.core.tree.rtree import RTree

from pyske.core.util import fun

import operator

def test_b2r_r2b():
    rt = RTree('1', SList([RTree('2'),
                           RTree('3', SList([RTree('5'), RTree('6')])),
                           RTree('4')]))
    res = RLTree.from_rt(rt).to_rt()
    assert rt == res


def test_eq():
    rt1 = RTree('A', SList([RTree('B'),
                           RTree('C', SList([RTree('E'), RTree('F')])),
                           RTree('D')]))
    rt2 = RTree('1', SList([RTree('2'),
                           RTree('3', SList([RTree('5'), RTree('6')])),
                           RTree('4')]))
    res = RLTree.from_rt(rt1).zip(RLTree.from_rt(rt2)).map(lambda x: x[0] + x[1])
    exp = RLTree.from_rt(rt1.zip(rt2).map(lambda x: x[0] + x[1]))
    assert res == exp


def test_map():
    rt = RTree('1', SList([RTree('2'),
                           RTree('3', SList([RTree('5'), RTree('6')])),
                           RTree('4')]))
    res = RLTree.from_rt(rt).map(lambda x: int(x))
    exp = RLTree.from_rt(rt.map(lambda x: int(x)))
    assert res == exp


def test_map2():
    rt1 = RTree('A', SList([RTree('B'),
                           RTree('C', SList([RTree('E'), RTree('F')])),
                           RTree('D')]))
    rt2 = RTree('1', SList([RTree('2'),
                           RTree('3', SList([RTree('5'), RTree('6')])),
                           RTree('4')]))
    res = RLTree.from_rt(rt1).map2(lambda x, y: (x, y), RLTree.from_rt(rt2))
    exp = RLTree.from_rt(rt1.map2(lambda x, y: (x, y), rt2))
    assert res == exp


def test_zip():
    rt1 = RTree('A', SList([RTree('B'),
                           RTree('C', SList([RTree('E'), RTree('F')])),
                           RTree('D')]))
    rt2 = RTree('1', SList([RTree('2'),
                           RTree('3', SList([RTree('5'), RTree('6')])),
                           RTree('4')]))
    res = RLTree.from_rt(rt1).zip(RLTree.from_rt(rt2))
    exp = RLTree.from_rt(rt1.zip(rt2))
    assert res == exp


def test_reduce():
    rt = RTree(1, SList([RTree(2),
                           RTree(3, SList([RTree(5), RTree(6)])),
                           RTree(4)]))
    res = RLTree.from_rt(rt).reduce(fun.mult, 1, fun.add, 0)
    exp = rt.reduce(fun.mult, 1, fun.add, 0)
    assert res == exp


def test_uacc():
    rt = RTree(1, SList([RTree(2),
                           RTree(3, SList([RTree(5), RTree(6)])),
                           RTree(4)]))
    res = RLTree.from_rt(rt).uacc(fun.mult, 1, fun.add, 0).to_rt()
    exp = rt.uacc(fun.mult, 1, fun.add, 0)
    assert res == exp


def test_dacc():
    rt = RTree(15, SList([RTree(24),
                          RTree(32, SList([RTree(56),
                                           RTree(63)]
                                          )
                                ),
                          RTree(41)])
               )
    res = RLTree.from_rt(rt).dacc(operator.add, 0).to_rt()
    exp = rt.dacc(operator.add, 0)
    assert res == exp

# TODO
# def test_lacc():
#     rt = RTree(15, SList([RTree(24),
#                           RTree(32, SList([RTree(56),
#                                            RTree(63)]
#                                           )
#                                 ),
#                           RTree(41)])
#                )
#     res = RLTree.from_rt(rt).lacc(operator.add, 0).to_rt()
#     exp = rt.lacc(operator.add, 0)
#     print()
#     print(res)
#     print(exp)
#     assert res == exp

# TODO
# def test_racc():
#     rt = RTree(15, SList([RTree(24),
#                           RTree(32, SList([RTree(56),
#                                            RTree(63)]
#                                           )
#                                 ),
#                           RTree(41)])
#                )
#     res = RBTree.from_rt(rt).racc(operator.add, 0).to_rt()
#     exp = rt.racc(operator.add, 0)
#     assert res == exp
