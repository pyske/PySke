from pyske.btree import BTree, Node, Leaf
from pyske.ltree import serialization
from pyske.ptree import PTree
from pyske.support.parallel import *

import time

# --------------------- #

# bt = Node(1, Node(1, Node (1, Leaf (1), Leaf(1)), Node (1, Leaf (1), Leaf(1))), Leaf(1))
bt = Node(1, Node(2, Node (3, Leaf (4), Leaf(5)), Node (6, Leaf (7), Leaf(8))), Node(9, Leaf(10), Leaf(11)))
m = 3
lt = serialization(bt, m)

# --------------------- #

at_root(lambda : print("Linearized tree: " + str(lt)))

pt = PTree(lt)
print(pt)

time.sleep(1)

at_root(lambda : print("-----------"))


pt_map = pt.map(lambda x : "LEAF", lambda x : "NODE")
print(pt_map.browse())
# print(pt_map)
id_f = lambda x : x

time.sleep(1)
at_root(lambda : print("-----------"))

pt1 = pt.map(lambda x : 1, lambda x : 1)
sum3 = lambda x,y,z : x + y + z
print(pt1.browse())

time.sleep(4)
at_root(lambda : print("-----------"))

res = pt1.reduce(sum3, id_f, sum3, sum3, sum3)

at_root(lambda : print(res))
