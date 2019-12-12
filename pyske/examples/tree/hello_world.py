"""
Tree Examples
"""
import random
from pyske.core.support.generate import ill_balanced_btree, balanced_btree, random_btree
from pyske.core.tree.ltree import LTree
from pyske.core.tree.ptree import PTree
from pyske.core.util import par
from pyske.examples.tree.tree_functions import size, size_by_node, prefix, ancestors
from pyske.core.support import parallel


_COMM = parallel.COMM
_PID = parallel.PID
_NPROCS = parallel.NPROCS

_MSG = "hello world!"


def _rand_str():
    return _MSG[random.randint(0, len(_MSG) - 1)]


def _test(bin_tree):
    print(bin_tree)
    par.at_root(lambda: print("-----"))
    m_bridge_param = 3
    linear_tree = LTree.from_bt(bin_tree, m_bridge_param)
    parallel_tree = PTree(linear_tree)
    par.at_root(lambda: print(linear_tree))
    print(parallel_tree)
    par.at_root(lambda: print("-----"))
    res = prefix(parallel_tree)
    par.at_root(lambda: print("prefix result:"))
    print(res)
    par.at_root(lambda: print("-----"))
    res = size(parallel_tree)
    par.at_root(lambda: print("size result:"))
    print(res)
    par.at_root(lambda: print("-----"))
    res = size_by_node(parallel_tree)
    par.at_root(lambda: print("size_by_node result:"))
    print(res)
    par.at_root(lambda: print("-----"))
    res = ancestors(parallel_tree)
    par.at_root(lambda: print("ancestors result:"))
    print(res)


def _main():
    if _PID == 0:
        bal = balanced_btree(_rand_str, 15)
        ill = ill_balanced_btree(_rand_str, 15)
        rdm = random_btree(_rand_str, 15)
        for i in range(1, _NPROCS):
            _COMM.send({'b': bal, 'i': ill, 'r': rdm}, dest=i, tag=1)
    else:
        data = _COMM.recv(source=0, tag=1)
        bal = data['b']
        ill = data['i']
        rdm = data['r']
    par.barrier()
    par.at_root(lambda: print("\nBALANCED\n"))
    _test(bal)
    par.at_root(lambda: print("\nILL BALANCED\n"))
    _test(ill)
    par.at_root(lambda: print("\nRANDOM\n"))
    _test(rdm)


_main()
