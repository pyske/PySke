from pyske.ltree import LTree, Segment, TaggedValue, serialization
from pyske.btree import Node, Leaf
from pyske.test.run import run_tests

# -------------------------- #

def test_serialization_1_4():
	#btree4
	bt = Node(1, Node(2, Node (4, Leaf (6), Leaf(7)), Node (5, Leaf (8), Leaf(9))), Leaf(3))
	m = 4
	res = serialization(bt, m)
	seg1 = Segment([TaggedValue(1,"C")])
	seg2 = Segment([TaggedValue(2,"C")])
	seg3 = Segment([TaggedValue(4,"N"),TaggedValue(6,"L"),TaggedValue(7,"L")])
	seg4 = Segment([TaggedValue(5,"N"),TaggedValue(8,"L"),TaggedValue(9,"L")])
	seg5 = Segment([TaggedValue(3,"L")])
	exp = LTree([seg1, seg2, seg3, seg4, seg5])
	assert res == exp


def test_serialization_1_3():
	#btree4
	bt = Node(1, Node(2, Node (4, Leaf (6), Leaf(7)), Node (5, Leaf (8), Leaf(9))), Leaf(3))
	m = 3
	res = serialization(bt, m)
	seg1 = Segment([TaggedValue(1,"N"), TaggedValue(2,"C"), TaggedValue(3,"L")])
	seg2 = Segment([TaggedValue(4,"N"),TaggedValue(6,"L"),TaggedValue(7,"L")])
	seg3 = Segment([TaggedValue(5,"N"),TaggedValue(8,"L"),TaggedValue(9,"L")])
	exp = LTree([seg1, seg2, seg3])
	assert res == exp



def test_serialization_1_2():
	#btree4
	bt = Node(1, Node(2, Node (4, Leaf (6), Leaf(7)), Node (5, Leaf (8), Leaf(9))), Leaf(3))
	m = 2
	res = serialization(bt, m)
	seg1 = Segment([TaggedValue(1,"C")])
	seg2 = Segment([TaggedValue(2,"C")])
	seg3 = Segment([TaggedValue(4,"C")])
	seg4 = Segment([TaggedValue(6,"L")])
	seg5 = Segment([TaggedValue(7,"L")])
	seg6 = Segment([TaggedValue(5,"C")])
	seg7 = Segment([TaggedValue(8,"L")])
	seg8 = Segment([TaggedValue(9,"L")])
	seg9 = Segment([TaggedValue(3,"L")])
	exp = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9])
	assert res == exp


def test_serialization_1_1():
	#btree4
	bt = Node(1, Node(2, Node (4, Leaf (6), Leaf(7)), Node (5, Leaf (8), Leaf(9))), Leaf(3))
	m = 1
	res = serialization(bt, m)
	seg1 = Segment([TaggedValue(1,"C")])
	seg2 = Segment([TaggedValue(2,"C")])
	seg3 = Segment([TaggedValue(4,"C")])
	seg4 = Segment([TaggedValue(6,"L")])
	seg5 = Segment([TaggedValue(7,"L")])
	seg6 = Segment([TaggedValue(5,"C")])
	seg7 = Segment([TaggedValue(8,"L")])
	seg8 = Segment([TaggedValue(9,"L")])
	seg9 = Segment([TaggedValue(3,"L")])
	exp = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9])
	assert res == exp


def test_serialization_2_5():
	#btree5
	bt =  Node(13, Node(3, Leaf(1), Leaf(1)), Node(9, Node(7,Node(3, Leaf(1), Leaf(1)),Node(3, Leaf(1), Leaf(1))), Leaf(1)))
	m = 5
	res = serialization(bt, m)
	seg1 = Segment([TaggedValue(13,"C")])
	seg2 = Segment([TaggedValue(3,"N"),TaggedValue(1,"L"),TaggedValue(1,"L")])
	seg3 = Segment([TaggedValue(9,"N"),TaggedValue(7,"C"),TaggedValue(1,"L")])
	seg4 = Segment([TaggedValue(3,"N"),TaggedValue(1,"L"),TaggedValue(1,"L")])
	seg5 = Segment([TaggedValue(3,"N"),TaggedValue(1,"L"),TaggedValue(1,"L")])
	exp = LTree([seg1,seg2,seg3,seg4,seg5])
	assert res == exp


def test_serialization_2_4():
	#btree5
	bt =  Node(13, Node(3, Leaf(1), Leaf(1)), Node(9, Node(7,Node(3, Leaf(1), Leaf(1)),Node(3, Leaf(1), Leaf(1))), Leaf(1)))
	m = 4
	res = serialization(bt, m)
	seg1 = Segment([TaggedValue(13,"C")])
	seg2 = Segment([TaggedValue(3,"N"),TaggedValue(1,"L"),TaggedValue(1,"L")])
	seg3 = Segment([TaggedValue(9,"C")])
	seg4 = Segment([TaggedValue(7,"C")])
	seg5 = Segment([TaggedValue(3,"N"),TaggedValue(1,"L"),TaggedValue(1,"L")])
	seg6 = Segment([TaggedValue(3,"N"),TaggedValue(1,"L"),TaggedValue(1,"L")])
	seg7 = Segment([TaggedValue(1,"L")])
	exp = LTree([seg1,seg2,seg3,seg4,seg5,seg6,seg7])
	assert res == exp


def test_serialization_2_3():
	#btree5
	bt =  Node(13, Node(3, Leaf(1), Leaf(1)), Node(9, Node(7,Node(3, Leaf(1), Leaf(1)),Node(3, Leaf(1), Leaf(1))), Leaf(1)))
	m = 3
	res = serialization(bt, m)
	seg1 = Segment([TaggedValue(13,"C")])
	seg2 = Segment([TaggedValue(3,"N"),TaggedValue(1,"L"),TaggedValue(1,"L")])
	seg3 = Segment([TaggedValue(9,"N"),TaggedValue(7,"C"),TaggedValue(1,"L")])
	seg4 = Segment([TaggedValue(3,"N"),TaggedValue(1,"L"),TaggedValue(1,"L")])
	seg5 = Segment([TaggedValue(3,"N"),TaggedValue(1,"L"),TaggedValue(1,"L")])
	exp = LTree([seg1,seg2,seg3,seg4,seg5])
	assert res == exp


def test_serialization_2_2():
	#btree5
	bt =  Node(13, Node(3, Leaf(1), Leaf(1)), Node(9, Node(7,Node(3, Leaf(1), Leaf(1)),Node(3, Leaf(1), Leaf(1))), Leaf(1)))
	m = 2
	res = serialization(bt, m)
	seg1 = Segment([TaggedValue(13,"C")])
	seg2 = Segment([TaggedValue(3,"C")])
	seg3 = Segment([TaggedValue(1,"L")])
	seg4 = Segment([TaggedValue(1,"L")])
	seg5 = Segment([TaggedValue(9,"C")])
	seg6 = Segment([TaggedValue(7,"C")])
	seg7 = Segment([TaggedValue(3,"C")])
	seg8 = Segment([TaggedValue(1,"L")])
	seg9 = Segment([TaggedValue(1,"L")])
	seg10 = Segment([TaggedValue(3,"C")])
	seg11 = Segment([TaggedValue(1,"L")])
	seg12 = Segment([TaggedValue(1,"L")])
	seg13 = Segment([TaggedValue(1,"L")])
	exp = LTree([seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9, seg10, seg11, seg12, seg13])
	assert res == exp

tests_serialization = [test_serialization_1_4,test_serialization_1_3,test_serialization_1_2,test_serialization_1_1,test_serialization_2_5,test_serialization_2_4,test_serialization_2_3,test_serialization_2_2]

# -------------------------- #

#TODO

tests_deserialization = []

# -------------------------- #

fcts = tests_deserialization + tests_serialization 

run_tests(fcts, "serialization")
