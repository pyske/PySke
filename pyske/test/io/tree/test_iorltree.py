import random

from pyske.core import SList
from pyske.core.io.tree.iorltree import IORLTree
from pyske.core.tree import RLTree, RTree


def _randint():
    return random.randint(1, 101)


def test_write_read_delete_exists():
    filename = "test"
    rt = RTree(1, SList([RTree(2),
                         RTree(3, SList([RTree(5), RTree(6)])),
                         RTree(4)]))
    exp = RLTree.from_rt(rt)
    IORLTree.write(filename, exp)
    assert IORLTree.exists(filename)
    res = IORLTree.read(filename)
    assert res == exp
    IORLTree.remove(filename)
    assert not IORLTree.exists(filename)
