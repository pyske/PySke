from pyske.slist import SList
from pyske.btree import Node, Leaf
from pyske.rtree import RNode
from pyske.ltree import VTag, TaggedValue, Segment, LTree, serialization, parseVTag
from pyske.errors import NotEqualSizeError

# ------------------------------------ #

rt5 = RNode(5, SList())
rt6 = RNode(6, SList())
rt2 = RNode(2, SList())
rt3 = RNode(3, SList([rt5, rt6]))
rt4 = RNode(4, SList())
rt1 = RNode(1, SList([rt2, rt3, rt4]))
print(rt1)
bt = rt1.r2b()
print(bt)
rt = RNode(bt)
print(rt)

# ------------------------------------ #
l0 = SList([])
l1 = SList()
print(l0 == l1) # True
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

l0 = SList([1, 1, 1, 1, 1, 1, 1, 1, 1])
l1 = l0.scan2(lambda x, y: x + y, 0)
print(l1)

# ------------------------------------ #

bt0 = Node(1,Leaf(2),Node(3,Leaf(4),Leaf(4)))
bt1 = bt0.map(lambda x: 1, lambda x: 1)
size = bt1.reduce(lambda x,y,z: x+y+z)
print("size = " + str(size))

# ------------------------------------ #

print("SERIALIZATION")
bt0 = Node(1,Leaf(2),Node(3,Leaf(4),Leaf(4)))
print(str(serialization(bt0, 2)))

# ------------------------------------ #

print("LTREE")
tv1 = TaggedValue(1, "C")
tv2 = TaggedValue(2, "L")
tv3 = TaggedValue(3, "L")
seg1 = Segment([tv1, tv2, tv3])
lt0 = LTree([seg1])

vals = [2,3,4]
try:
	lt1 = lt0.replace_values(vals)
	print(str(lt1))
except NotEqualSizeError as e:
	print(str(e))


# ------------------------------------ #
