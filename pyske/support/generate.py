from pyske.btree import BTree, Leaf, Node
from pyske.slist import SList

import random
import sys



def generate_random_list(frdm, len):
	res = SList([])
	for i in range(len):
		res.append(frdm())
	return res


def generate_balanced_btree(frdm, size):
	size = (size if size%2 == 1 else size + 1)
	if size == 1:
		return Leaf(frdm())
	else:
		left = generate_balanced_btree(frdm, (size-3)/2 + 1)
		right = generate_balanced_btree(frdm, (size-3)/2 + 1)
		return Node(frdm(), left, right)


def __insert_values_btree(v1, v2, bt):
	if bt.is_leaf():
		return Node(bt.get_value(), Leaf(v1), Leaf(v2))
	else: # bt.is_node()
		rdm = random.randint(1,101)
		if rdm > 50 :
			# insert left
			left = __insert_values_btree(v1,v2, bt.get_left())
			right = bt.get_right()
			return Node(bt.get_value(), left, right)
		else:
			# insert right
			left = bt.get_left()
			right = __insert_values_btree(v1,v2, bt.get_right())
			return Node(bt.get_value(), left, right)
			

def generate_random_btree(frdm, size):
	adj_size = (size if size%2 == 1 else size + 1)
	values = generate_random_list(frdm, adj_size)
	bt = Leaf(values[0])
	for i in range(1, len(values), 2):
		bt = __insert_values_btree(values[i], values[i+1], bt)
	return bt


def generate_illbalanced_btree(frdm, size):
	size = (size if size%2 == 1 else size + 1)
	def aux(size, continuation):
		if size == 1:
			return continuation(Leaf(frdm()))
		else:
			return aux(size-2, lambda tr : continuation(Node(frdm(), Leaf(frdm()), tr)) )
	return aux(size, lambda x : x)



