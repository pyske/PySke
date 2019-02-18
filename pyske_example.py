from pyske.btree import BTree, Node, Leaf
from pyske.ltree import LTree
from pyske.applications.prefix import prefix
from pyske.support.generate import *

import random

frdm = lambda : random.randint(1,101)
bt = generate_balanced_btree(frdm, 10)
# bt = generate_illbalanced_btree(frdm, 10)
# bt = generate_random_btree(frdm, 10)
print(bt)

print("-----")

m = 3
lt = LTree.init_from_bt(bt, m)
print(lt)

print("-----")

res = prefix(lt)
print(res)


