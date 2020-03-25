import random

from pyske.core.io.tree.iodistribution import IODistribution
from pyske.core.io.tree.ioptree import IOPTree
from pyske.core.support import parallel
from pyske.core.tree import LTree
from pyske.core.tree.distribution import Distribution


from pyske.core.support.generate import balanced_btree
from pyske.core.io.tree.ioltree import *
from pyske.core.tree.ptree import PTree


def _randint():
    return random.randint(1, 101)


def test_split():
    filename = "test"
    # init nb proc
    tmp = parallel.NPROCS
    parallel.NPROCS = 3

    bt = balanced_btree(_randint, 20)
    lt = LTree.from_bt(bt, 3)
    sizes = []
    for seg in lt:
        sizes.append(seg.length)
    dist = Distribution.balanced_tree(sizes)
    IODistribution.write(filename, dist)
    IOLTree.write(filename, lt)

    IOPTree.split(filename, filename)

    IODistribution.remove(filename)
    IOLTree.remove(filename)
    IOPTree.removeall(filename)

    # reset nb proc
    parallel.NPROCS = tmp

    assert not IODistribution.exists(filename)
    assert not IOLTree.exists(filename)
    assert not IOPTree.exists(filename)


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


