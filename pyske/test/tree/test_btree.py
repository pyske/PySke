from pyske.core.tree.btree import BTree, Leaf, Node
from pyske.core.support.errors import NotEqualSizeError

# -------------------------- #

def test_is_leaf_true():
	bt = Leaf(1)
	exp = True
	res = bt.is_leaf()
	assert exp == res


def test_is_leaf_false():
	bt = Node(1, Leaf(1), Leaf(1))
	exp = False
	res = bt.is_leaf()
	assert exp == res

# -------------------------- #

def test_is_node_false():
	bt = Leaf(1)
	exp = False
	res = bt.is_node()
	assert exp == res


def test_is_node_true():
	bt = Node(1, Leaf(1), Leaf(1))
	exp = True
	res = bt.is_node()
	assert exp == res

# -------------------------- #

def test_map_leaf():
	bt = Leaf(1)
	kl = lambda x : x + 1
	kn = lambda x : x - 1
	res = bt.map(kl, kn)
	exp = Leaf(2)
	assert exp == res


def test_map_node():
	bt = Node(1, Leaf(2), Leaf(3))
	kl = lambda x : x + 1
	kn = lambda x : x - 1
	res = bt.map(kl, kn)
	exp = Node(0, Leaf(3), Leaf(4))
	assert exp == res

# -------------------------- #

def test_mapt_leaf():
	bt = Leaf(1)
	kl = lambda x : x + 1
	kn = lambda x,y,z : max(x,max(y.get_value(),z.get_value()))
	res = bt.mapt(kl, kn)
	exp = Leaf(2)
	assert exp == res


def test_mapt_node():
	bt = Node(1, Leaf(2), Leaf(3))
	kl = lambda x : x + 1
	kn = lambda x,y,z : max(x,max(y.get_value(),z.get_value()))
	res = bt.mapt(kl, kn)
	exp = Node(3, Leaf(3), Leaf(4))
	assert exp == res

# -------------------------- #

def test_reduce_leaf():
	bt = Leaf(2)
	k = lambda x,y,z : max(x,max(y,z))
	res = bt.reduce(k)
	exp = 2
	assert exp == res


def test_reduce_node():
	bt = Node(1, Leaf(2), Leaf(3))
	k = lambda x,y,z : max(x,max(y,z))
	res = bt.reduce(k)
	exp = 3
	assert exp == res

# -------------------------- #

def test_uacc_leaf():
	bt = Leaf(1)
	k = lambda x,y,z : x + y + z
	res = bt.uacc(k)
	exp = Leaf(1)
	assert exp == res


def test_uacc_node():
	bt = Node(1, Leaf(2), Leaf(3))
	k = lambda x,y,z : x + y + z
	res = bt.uacc(k)
	exp =  Node(6, Leaf(2), Leaf(3))
	assert exp == res

# -------------------------- #

def test_dacc_leaf():
	c = 0
	bt = Leaf(1)
	gl = lambda x, y : x+y
	gr = lambda x, y : 0 if x-y < 0 else x-y
	res = bt.dacc(gl, gr, c)
	exp = Leaf(c)
	assert exp == res


def test_dacc_node():
	c = 0
	bt = Node(1, Node(2, Leaf(3), Leaf(4)), Leaf(5))
	gl = lambda x, y : x+y
	gr = lambda x, y : 0 if x-y < 0 else x-y
	res = bt.dacc(gl, gr, c)
	exp = Node(0, Node(1, Leaf(3), Leaf(0)), Leaf(0))
	assert exp == res

# -------------------------- #

def test_zip_leaf():
	bt1 = Leaf(1) 
	bt2 = Leaf(2)
	exp = Leaf((1,2))
	res = bt1.zip(bt2)
	assert exp == res


def test_zip_node():
	bt1 = Node(1, Leaf(2), Leaf(3))
	bt2 = Node(4, Leaf(5), Leaf(6))
	exp = Node((1,4), Leaf((2,5)), Leaf((3,6)))
	res = bt1.zip(bt2)
	assert exp == res


def test_zip_leaf_node():
	bt1 = Leaf(1) 
	bt2 = Node(4, Leaf(5), Leaf(6))
	try:
		bt1.zip(bt2)
		raise TestFailure()
	except NotEqualSizeError as e:
		assert True


def test_zip_node_leaf():
	bt1 = Node(1, Leaf(2), Leaf(3))
	bt2 = Leaf(2)
	try:
		bt1.zip(bt2)
		raise TestFailure()
	except NotEqualSizeError as e:
		assert True

# -------------------------- #

def test_zipwith_leaf():
	bt1 = Leaf(1) 
	bt2 = Leaf(2)
	f = lambda x,y : x + y
	exp = Leaf(3)
	res = bt1.zipwith(bt2,f)
	assert exp == res


def test_zipwith_node():
	bt1 = Node(1, Leaf(2), Leaf(3))
	bt2 = Node(4, Leaf(5), Leaf(6))
	f = lambda x,y : x + y
	exp = Node(5, Leaf(7), Leaf(9))
	res = bt1.zipwith(bt2,f)
	assert exp == res


def test_zipwith_leaf_node():
	bt1 = Leaf(1) 
	bt2 = Node(4, Leaf(5), Leaf(6))
	f = lambda x,y : x + y
	try:
		bt1.zipwith(bt2,f)
		raise TestFailure()
	except NotEqualSizeError as e:
		assert True


def test_zipwith_node_leaf():
	bt1 = Node(1, Leaf(2), Leaf(3))
	bt2 = Leaf(2)
	f = lambda x,y : x + y
	try:
		bt1.zipwith(bt2,f)
		raise TestFailure()
	except NotEqualSizeError as e:
		assert True

# -------------------------- #

def test_getchl_leaf():
	c = 1
	bt = Leaf(3)
	res = bt.getchl(c)
	exp = Leaf(c)
	assert res == exp


def test_getchl_node_right():
	c = 1
	bt = Node(3, Leaf(2), Node(4, Leaf(2), Leaf(6)))
	res = bt.getchl(c)
	exp = Node(2, Leaf(c), Node(2, Leaf(c), Leaf(c)))
	assert res == exp


def test_getchl_node_left():
	c = 1
	bt = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
	res = bt.getchl(c)
	exp =  Node(4, Node(2, Leaf(c), Leaf(c)), Leaf(c))
	assert res == exp

# -------------------------- #

def test_getchr_leaf():
	c = 1
	bt = Leaf(3)
	res = bt.getchr(c)
	exp = Leaf(c)
	assert res == exp


def test_getchr_node_right():
	c = 1
	bt = Node(3, Leaf(2), Node(4, Leaf(2), Leaf(6)))
	res = bt.getchr(c)
	exp = Node(4, Leaf(c), Node(6, Leaf(c), Leaf(c)))
	assert res == exp


def test_getchr_node_left():
	c = 1
	bt = Node(3, Node(4, Leaf(2), Leaf(6)), Leaf(2))
	res = bt.getchr(c)
	exp =  Node(2, Node(6, Leaf(c), Leaf(c)), Leaf(c))
	assert res == exp


# -------------------------- #
