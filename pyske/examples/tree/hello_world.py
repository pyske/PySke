import random
from pyske.core.support.generate import *
from pyske.core.tree.ltree import LTree
from pyske.core.tree.ptree import PTree
from pyske.core.util import par
from pyske.examples.tree.prefix import prefix
from pyske.examples.tree.size import size
from pyske.examples.tree.size_by_node import size_by_node
from pyske.core.support import parallel
from pyske.core.util import fun

comm = parallel.COMM
pid = parallel.PID
nprocs = parallel.NPROCS

msg = "hello world!"


def plus1(x, y):
    return x + y + 1


def ancestors(tree):
    return tree.map(fun.zero, fun.zero).dacc(plus1, plus1, 0, fun.idt, fun.idt, plus1, plus1)


def frdm(_):
    return msg[random.randint(0, len(msg) - 1)]


def test(bt):
    print(bt)
    par.at_root(lambda: print("-----"))
    m = 3
    lt = LTree.init_from_bt(bt, m)
    pt = PTree(lt)
    par.at_root(lambda: print(lt))
    print(pt)
    par.at_root(lambda: print("-----"))
    res = prefix(pt)
    par.at_root(lambda: print("prefix result:"))
    print(res)
    par.at_root(lambda: print("-----"))
    res = size(pt)
    par.at_root(lambda: print("size result:"))
    print(res)
    par.at_root(lambda: print("-----"))
    res = size_by_node(pt)
    par.at_root(lambda: print("size_by_node result:"))
    print(res)
    par.at_root(lambda: print("-----"))
    res = ancestors(pt)
    par.at_root(lambda: print("ancestors result:"))
    print(res)


data = {}
if pid == 0:
    bal = balanced_btree(frdm, 15)
    ill = ill_balanced_btree(frdm, 15)
    rdm = random_btree(frdm, 15)
    for i in range(1, nprocs):
        comm.send({'b': bal, 'i': ill, 'r': rdm}, dest=i, tag=1)
else:
    data = comm.recv(source=0, tag=1)
bal = data['b']
ill = data['i']
rdm = data['r']

par.barrier()

par.at_root(lambda: print("\nBAlANCED\n"))
test(bal)
par.at_root(lambda: print("\nILL BAlANCED\n"))
test(ill)
par.at_root(lambda: print("\nRANDOM\n"))
test(rdm)
