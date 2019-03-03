from pyske.test.support.run import run_tests
from pyske.core.tree.rtree import RNode
from pyske.core.tree.btree import Node, Leaf 
from pyske.core.list.slist import SList
from pyske.core.support.errors import ConstructorError
from pyske.test.support.errors import TestFailure


# -------------------------- #

def test_b2r_leaf_none():
	bt = Leaf(None)
	try:
		RNode(bt)
		raise TestFailure()
	except ConstructorError as e:
		assert True


def test_b2r_leaf():
	bt = Leaf(1)
	res = RNode(bt)
	exp = RNode(1)
	assert res == exp


def test_b2r_node_from_rt():
	bt = Node(1, 
		Node(2, 
			Leaf(None), 
			Node(3, 
				Node(5, 
					Leaf(None), 
					Node(6, 
						Leaf(None), 
						Leaf(None)
						)
					), 
				Node(4, 
					Leaf(None), 
					Leaf(None)
					)
				)
			), 
		Leaf(None)
		)
	rn5 = RNode(5)
	rn6 = RNode(6)
	rn3 = RNode(3, SList([rn5, rn6]))
	rn2 = RNode(2)
	rn4 = RNode(4)
	exp = RNode(1, SList([rn2, rn3, rn4]))
	res = RNode(bt)

	assert res == exp

tests_b2r = [test_b2r_leaf_none, test_b2r_leaf, test_b2r_node_from_rt]

# -------------------------- #

def test_r2b_1():
	ch = SList()
	ch.append(RNode(2))
	ch.append(RNode(3))
	rn = RNode(1, ch)
	res = rn.r2b()
	exp = Node(1, Node(2, Leaf(None), Node(3,Leaf(None), Leaf(None))), Leaf(None))
	assert res == exp


def test_r2b_2():
	rn5 = RNode(5)
	rn6 = RNode(6)
	rn3 = RNode(3, SList([rn5, rn6]))
	rn2 = RNode(2)
	rn4 = RNode(4)
	rn1 = RNode(1, SList([rn2, rn3, rn4]))
	res = rn1.r2b()
	exp = \
	Node(1, 
		Node(2, 
			Leaf(None), 
			Node(3, 
				Node(5, 
					Leaf(None), 
					Node(6, 
						Leaf(None), 
						Leaf(None)
						)
					), 
				Node(4, 
					Leaf(None), 
					Leaf(None)
					)
				)
			), 
		Leaf(None)
		)
	assert res == exp

tests_r2b = [test_r2b_1, test_r2b_2]

# -------------------------- #

#TODO

tests_add_children = []

# -------------------------- #

#TODO

tests_map = []

# -------------------------- #

#TODO

tests_reduce = []

# -------------------------- #

#TODO

tests_uacc = []

# -------------------------- #

#TODO

tests_dacc = []

# -------------------------- #

#TODO

tests_lacc = []

# -------------------------- #

#TODO

tests_racc = []

# -------------------------- #

#TODO

tests_zip = []

# -------------------------- #



tests_zipwith = []

# -------------------------- #


fcts = tests_b2r + tests_r2b \
	+ tests_add_children + tests_map + tests_reduce \
	+ tests_uacc + tests_dacc + tests_lacc + tests_racc \
	+ tests_zip + tests_zipwith


run_tests(fcts, "rtree")