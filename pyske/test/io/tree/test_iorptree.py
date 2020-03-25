import random

from pyske.core import SList
from pyske.core.io.tree.iodistribution import IODistribution
from pyske.core.io.tree.ioptree import IOPTree
from pyske.core.io.tree.iorltree import IORLTree
from pyske.core.io.tree.iorptree import IORPTree
from pyske.core.support import parallel
from pyske.core.tree import LTree, RTree, RLTree
from pyske.core.tree.distribution import Distribution


from pyske.core.support.generate import balanced_btree
from pyske.core.io.tree.ioltree import *
from pyske.core.tree.ptree import PTree


def _randint():
    return random.randint(1, 101)


def test_split():
    # SETUP
    tmp = parallel.NPROCS
    parallel.NPROCS = 3  # init nb proc

    filename = "test"
    rt = RTree(1, SList([RTree(2),
                         RTree(3, SList([RTree(5), RTree(6)])),
                         RTree(4)]))
    rlt = RLTree.from_rt(rt)
    sizes = []
    for seg in rlt.lt:
        sizes.append(seg.length)
    dist = Distribution.balanced_tree(sizes)
    IODistribution.write(filename, dist)
    IORLTree.write(filename, rlt)

    # TEST
    IORPTree.split(filename, filename, filename)

    # WRAP UP
    IODistribution.remove(filename)
    IORLTree.remove(filename)
    IORPTree.removeall(filename)
    assert not IODistribution.exists(filename)
    assert not IOLTree.exists(filename)
    assert not IOPTree.exists(filename)
    parallel.NPROCS = tmp  # reset nb proc


def test_write_read_delete_exists():
    filename = "test"
    bt = balanced_btree(_randint, 100)
    exp = PTree.from_bt(bt, 10)
    IOPTree.write(filename, exp)
    assert IOPTree.exists(filename)
    res = IOPTree.read(filename, parser=int)
    assert exp == res
    IOPTree.remove(filename)
    assert not IOPTree.exists(filename)
