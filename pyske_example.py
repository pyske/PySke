from pyske.slist import SList
from pyske.btree import Node, Leaf
from pyske.ltree import VTag, TaggedValue, Segment, LTree
from pyske.errors import NotEqualSizeError

# ------------------------------------ #

l0 = SList([3, 1, 4, 1, 5, 9, 2, 6, 5])
print(l0)
l1 = l0.map(lambda x: x - 1)
print(l1)
l1.append(1)

try:
	l0.zip(l1)
except NotEqualSizeError as e:
	print(str(e))

# ------------------------------------ #

bt0 = Node(1,Leaf(2),Node(3,Leaf(4),Leaf(4)))
bt1 = bt0.map(lambda x: 1, lambda x: 1)
size = bt1.reduce(lambda x,y,z: x+y+z)
print("size = " + str(size))

# ------------------------------------ #

tv1 = TaggedValue(1, "C")
tv2 = TaggedValue(2, "L")
tv3 = TaggedValue(3, "L")
seg1 = Segment([tv1, tv2, tv3])
lt0 = LTree([seg1])

vals = [2,3,4]
try:
	lt1 = lt0.replace_values(vals)
except NotEqualSizeError as e:
	print(str(e))

print(str(lt1))

# ------------------------------------ #
