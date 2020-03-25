import random

from pyske.core.support.generate import balanced_btree
from pyske.core.io.tree.ioltree import *
from pyske.core.tree import LTree


def _randint():
    return random.randint(1, 101)


def test_write_read_delete_exists():
    filename = "test"
    bt = balanced_btree(_randint, 10)
    exp = LTree.from_bt(bt, 3)
    IOLTree.write(filename, exp)
    assert IOLTree.exists(filename)
    res = IOLTree.read(filename)
    assert exp == res
    IOLTree.remove(filename)
    assert not IOLTree.exists(filename)

