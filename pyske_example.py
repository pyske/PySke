from pyske.structure.tree.btree import *
from pyske.structure.tree.ltree import *
from pyske.structure.tree.serialization import *

t = Node(1, Leaf(2), Leaf(3))
st = serialization(t, 3)
print(st)