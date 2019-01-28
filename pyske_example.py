from pyske.btree import BTree, Node, Leaf
from pyske.ltree import serialization
from pyske.applications.prefix import prefix


bt = Node(1, Node(2, Node (4, Leaf (6), Leaf(7)), Node (5, Leaf (8), Leaf(9))), Leaf(3))
m = 3
lt = serialization(bt, m)

res = prefix(lt)
print(res)