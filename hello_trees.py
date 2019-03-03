import random

from pyske.core.tree.btree import BTree, Node, Leaf
from pyske.core.tree.ltree import LTree
from pyske.core.tree.ptree import PTree

from pyske.core.support.generate import *
from pyske.core.support.parallel import *

from pyske.application.tree .prefix import prefix
from pyske.application.tree.size import size
from pyske.application.tree.size_by_node import size_by_node
from pyske.application.tree.ancestors import ancestors

msg = "hello world!"
frdm = lambda : msg[random.randint(0,len(msg)-1)]

def test(bt):
	print (bt)
	at_root(lambda : print("-----"))

	m = 3
	lt = LTree.init_from_bt(bt, m)
	pt = PTree(lt)
	at_root(lambda : print(lt))
	print(pt)

	at_root(lambda : print("-----"))

	res = prefix(pt)
	at_root(lambda : print("prefix result:"))
	print(res)

	at_root(lambda : print("-----"))

	res = size(pt)
	at_root(lambda : print("size result:"))
	print(res)

	at_root(lambda : print("-----"))

	res = size_by_node(pt)
	at_root(lambda : print("size_by_node result:"))
	print(res)

	at_root(lambda : print("-----"))
	res = ancestors(pt)
	at_root(lambda : print("ancestors result:"))
	print(res)

msg = "hello world!"
frdm = lambda : msg[random.randint(0,len(msg)-1)]

if pid == 0:
	bal = generate_balanced_btree(frdm, 15)
	ill = generate_illbalanced_btree(frdm, 15)
	rdm = generate_random_btree(frdm, 15)
	for i in range(1, nprocs):
		comm.send({'b' : bal, 'i' : ill, 'r' : rdm}, dest=i, tag=1)
else:
	data = comm.recv(source=0, tag=1)
	bal = data['b']
	ill = data['i']
	rdm = data['r']

comm.Barrier()

at_root(lambda : print("\nBAlANCED\n"))
test(bal)

at_root(lambda :print("\nILL BAlANCED\n"))
test(ill)

at_root(lambda :print("\nRANDOM\n"))
test(rdm)


