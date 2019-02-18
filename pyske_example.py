from pyske.btree import BTree, Node, Leaf
from pyske.ltree import LTree
from pyske.applications.prefix import prefix
from pyske.applications.size import size
from pyske.applications.size_by_node import size_by_node
from pyske.applications.ancestors import ancestors
from pyske.support.generate import *

import random

frdm = lambda : random.randint(1,101)
bt = generate_balanced_btree(frdm, 15)
# bt = generate_illbalanced_btree(frdm, 15)
# bt = generate_random_btree(frdm, 15)
print(bt)

print("-----")

m = 3
lt = LTree.init_from_bt(bt, m)
print(lt)

print("-----")

res = prefix(lt)
print("prefix result:\n" + str(res))

print("-----")

res = size(lt)
print("size result:\n" + str(res))

print("-----")

res = size_by_node(lt)
print("size_by_node result:\n" + str(res))

print("-----")

res = ancestors(lt)
print("ancestors result:\n" + str(res))


