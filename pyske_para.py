from pyske.btree import BTree, Node, Leaf
from pyske.ltree import serialization
from pyske.ptree import PTree
from pyske.support.parallel import *

import time


# --------------------- #

# Example : Prefix problem 

# --------------------- #

phi = lambda b : (1, 0, 0, 1)

def k(l, b, r):
	(ll, ls) = l
	(rl, rs) = r
	return (ls, ls + 1 + rs)
	

def psi_n(l, b, r):
	(ll, ls) = l
	(b0, b1, b2, b3) = b
	(rl, rs) = r
	res_1 = b0 * ls + b1 * (ls + rs + 1) + b2
	res_2 = ls + 1 + rs + b3
	return (res_1, res_2)


def psi_l(l, b, r):
	(l0, l1, l2, l3) = l
	(b0, b1, b2, b3) = b
	(rl, rs) = r
	res_0 = 0
	res_1 = b0 + b1
	res_2 = (b0 + b1) * l3 + b1 * (1 + rs) + b2
	res_3 = l3 + 1 + rs + b3
	return (res_0, res_1, res_2, res_3)


def psi_r(l, b, r):
	(ll, ls) = l
	(b0, b1, b2, b3) = b
	(r0, r1, r2, r3) = r
	res_0 = 0
	res_1 = b1
	res_2 = b1 * r3 + b0 * ls + b1 * (1 + ls) + b2
	res_3 = r3 + 1 + ls + b3
	return (res_0, res_1, res_2, res_3)

# --------------------- #

def gl(c, b):
	(bl, bs) = b
	return c + 1

def gr(c, b):
	(bl, bs) = b
	return c + bl + 1

def phi_l(b):
	(bl, bs) = b
	return 1

def phi_r(b):
	(bl, bs) = b
	return bl+1

sum2 = lambda x,y : x + y
# --------------------- #

bt = Node(1, Node(2, Node (3, Leaf (4), Leaf(5)), Node (6, Leaf (7), Leaf(8))), Node(9, Leaf(10), Leaf(11)))
m = 3
lt = serialization(bt, m)

# --------------------- #

pt = PTree(lt)
pt_mapped = pt.map(lambda a : (0,1), lambda x : x)
pt_uacc = pt_mapped.uacc(k, phi, psi_n, psi_l, psi_r)
pt_dacc = pt_uacc.dacc(gl, gr, 0, phi_l, phi_r, sum2, sum2)
print(pt_dacc.browse())

# --------------------- #
time.sleep(4)

lt_mapped = lt.map(lambda a : (0,1), lambda x : x)
lt_uacc = lt_mapped.uacc(k, phi, psi_n, psi_l, psi_r)
lt_dacc = lt_uacc.dacc(gl, gr, 0, phi_l, phi_r, sum2, sum2)
at_root(lambda : print(lt_dacc))




