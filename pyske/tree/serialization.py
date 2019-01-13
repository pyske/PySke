from .btree import Leaf, Node
from .ltree import VType, Value

def tv2lv(bt):
	"""
	Transforms a tagged Binary Tree in a list of segments, which are lists of Value
	"""
	tval = bt.get_value()
	if bt.is_leaf():
		return [[tval]] #the value of t has the shape: Value(Type.LEAF, val)
	else: #t.is_node()
		res_left  = tv2lv(bt.get_left())
		res_right = tv2lv(bt.get_right())
		if tval.isCritical():
			res=[[tval]]
			res.extend(res_left)
			res.extend(res_right)
			return res
		else: #tval.isNode()
			res_0 = [tval]
			res_0.extend(res_left[0])
			res_0.extend(res_right[0])
			res = [res_0]
			res.extend(res_left[1:])
			res.extend(res_right[1:])
			return res

def serialization(bt, m):
	"""
	Transforms a BTree into a list of (list of Value), called Segments from a critical value m.
	(Inspired by m-bridge algorithm)

	The process is composed by several steps:
		1. The a new BTree is created where each value corresponds to size of the current BTree
		2. Each node is tagged by a VType, which depends on m
		3. The initial tree, and the tagged tree are zipped and tuples within the leaves/nodes
			are transformed using the Value type
		4. The resulting tree is decomposed into a list of list of Value by splitting the tree on
			critical nodes

	Parameters
	----------
	bt : BTree
		The Binary Tree to serialize
	m : int
		The critical value used to defined critical nodes
	"""

	def getNodeType(v, l, r):
		"""
		Internal function used to determine what VType is associated to a Node,
		in a particular context (depending on m). 
		"""
		div_up = lambda n, m: (n / m + (0 if n % m == 0 else 1))
		top_left_by_m = div_up(l.get_value(), m)
		top_right_by_m = div_up(r.get_value(), m)
		val_by_m = div_up(v, m)
		if val_by_m > top_left_by_m and val_by_m > top_right_by_m:
			return VType.CRITICAL
		else:
			return VType.NODE

	# Step 1
	mapped = bt.map(lambda x: 1, lambda x: 1)
	sized = mapped.uacc(lambda a, b, c : a + b + c) 
	# Step 2
	tagged = sized.mapt(lambda x: VType.LEAF, getNodeType)
	# Step 3
	zipped = bt.zip(tagged)
	valued = zipped.map(lambda x: Value(x[0],x[1]), lambda x: Value(x[0],x[1]))
	# Step 4
	serial = tv2lv(valued)
	return serial