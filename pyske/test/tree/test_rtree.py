import operator

from pyske.core.list.slist import SList
from pyske.core.tree.rtree import RTree


def test_map():
    def f(x):
        return str(x)
    rt = RTree(15, SList([RTree(24),
                          RTree(32, SList([RTree(56),
                                           RTree(63)]
                                          )
                                ),
                          RTree(41)])
               )
    res = rt.map(f)
    exp = RTree(f(15), SList([RTree(f(24)),
                              RTree(f(32), SList([RTree(f(56)),
                                                  RTree(f(63))]
                                                 )
                                    ),
                              RTree(f(41))]))
    assert res == exp


def test_reduce():
    rt = RTree(15, SList([RTree(24),
                          RTree(32, SList([RTree(56),
                                           RTree(63)]
                                          )
                                ),
                          RTree(41)])
               )
    res = rt.reduce(operator.add, 0, operator.mul, 1)
    exp = 3503055
    assert res == exp


def test_uacc():
    rt = RTree(15, SList([RTree(24),
                          RTree(32, SList([RTree(56),
                                           RTree(63)]
                                          )
                                ),
                          RTree(41)])
               )
    res = rt.uacc(operator.add, 0, operator.mul, 1)
    exp = RTree(3503055, SList([RTree(24),
                                RTree(3560, SList([RTree(56),
                                                   RTree(63)]
                                                  )
                                      ),
                                RTree(41)])
                )
    assert res == exp


def test_dacc():
    rt = RTree(15, SList([RTree(24),
                          RTree(32, SList([RTree(56),
                                           RTree(63)]
                                          )
                                ),
                          RTree(41)])
               )
    exp = RTree(0, SList([RTree(15),
                          RTree(15, SList([RTree(47),
                                           RTree(47)])),
                          RTree(15)])
                )
    res = rt.dacc(operator.add, 0)
    assert res == exp


def test_lacc():
    rt = RTree(15, SList([RTree(24),
                          RTree(32, SList([RTree(56),
                                           RTree(63)]
                                          )
                                ),
                          RTree(41)])
               )
    res = rt.lacc(operator.add, 0)
    exp = RTree(0, SList([RTree(73),
                          RTree(41, SList([RTree(63),
                                           RTree(0)])
                                ),
                          RTree(0)])
                )
    assert res == exp


def test_racc():
    rt = RTree(15, SList([RTree(24),
                          RTree(32, SList([RTree(56),
                                           RTree(63)]
                                          )
                                ),
                          RTree(41)])
               )
    res = rt.racc(operator.add, 0)
    exp = RTree(0, SList([RTree(0),
                          RTree(24, SList([RTree(0),
                                           RTree(56)])
                                ),
                          RTree(56)])
                )
    assert res == exp
