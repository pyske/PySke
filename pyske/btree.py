from pyske.errors import NotEqualSizeError
from abc import ABC # abstract classes library

class BTree(ABC):
	"""
	An abstract class used to represent a Binary Tree

	...

	Methods
	-------
	is_leaf()
		Indicates if the BTree is a leaf   
	is_node()
		Indicates if the BTree is a node
	map(kl, kn)
		Applies kl to every leaf values of the Btree, and kn to every node values
	mapt(kl, kn)
		Applies kl to every leaf values the current instance, and kn to every subtrees that are nodes
	reduce(k)
		Reduces a BTree into a single value using k
	uacc(k)
		Makes an upward accumulation of the values in a BTree using k
	dacc(gl, gr, c)
		Makes an downward accumulation of the values in a BTree using gl, gr and c
	zip(t)
		Zip the values contained in t with the ones in the current instance
	"""

	def is_leaf(self):
		"""
		Indicates if the BTree is a leaf
		"""
		return False

	def is_node(self):
		"""
		Indicates if the BTree is a node
		"""
		return False
		

class Leaf(BTree):
	"""
	An extension of BTree. 
	A class used to represent a Leaf in a Binary Tree

	...
	
	Attributes
	----------
	value:
		A value describing the current leaf

	Methods
	-------
	is_leaf()
		Indicates if the BTree is a leaf   
	get_value()
		Get the value contained in the leaf
	set_value(v)
		Set the value contained in the leaf
	map(kl, kn)
		Applies kl to every leaf values of the Btree, and kn to every node values
	mapt(kl, kn)
		Applies kl to every leaf values the current instance, and kn to every subtrees that are nodes
	reduce(k)
		Reduces a BTree into a single value using k
	uacc(k)
		Makes an upward accumulation of the values in a BTree using k
	dacc(gl, gr, c)
		Makes an downward accumulation of the values in a BTree using gl, gr and c
	zip(t)
		Zip the values contained in t with the ones in the current instance
	"""
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return "leaf " + str(self.value)

	def is_leaf(self):
		return True

	def get_value(self):
		return self.value

	def set_value(self, v):
		self.value = v

	def map(self, kl, kn):
		"""
		Applies kl to every leaf values of the current instance, and kn to every node values

		Parameters
		----------
		kl : lambda x => y
			The function to apply to every leaf values of the current instance
		kn : lambda x => y
			The function to apply to every node values of the current instance
		"""
		return Leaf(kl(self.get_value()))

	def mapt(self, kl, kn):
		"""
		Applies kl to every leaf values the current instance, and kn to every subtrees that are nodes

		Parameters
		----------
		kl : lambda x => y
			The function to apply to every leaf values of the current instance
		kn : lambda x y z => r
			The function to apply to every node subtrees of the current instance
		"""
		return Leaf(kl(self.get_value()))

	def reduce(self, k):
		"""
		Reduces a BTree into a single value using k

		If the BTree is a leaf, the single reduced value is the value contained in the structure.
		
		Parameters
		----------
		k : lambda x y z => r
			The function used to reduce a BTree into a single value 
		"""
		return self.get_value()

	def uacc(self, k):
		"""
		Makes an upward accumulation of the values in the current instance using k

		If the BTree is a leaf, the tree doesn't change.

		Parameters
		----------
		k : lambda x y z => r
			The function used to reduce a BTree into a single value 
		"""
		return Leaf(self.get_value())

	def dacc(self, gl, gr, c):
		"""
		Makes an downward accumulation of the values in a BTree using gl, gr and c

		Parameters
		----------
		gl : lambda x y => z
			Function to make an accumulation to the left part of a node
		gr : lambda x y => z
			Function to make an accumulation to the right part of a node
		c : 
			Accumulator for the downward computation
		"""
		return Leaf(c)

	def zip(self, t):
		"""
		Zip the values contained in t with the ones in the current instance

		Parameters
		----------
		t : BTree
			The BTree to zip with the current instance

		Raises
		------
		NotEqualSizeError
			If the type of t is not the same one than the current instance
		"""
		if t.is_leaf():
			return Leaf((self.get_value(), t.get_value()))
		else:
			raise NotEqualSizeError('The two types of BTree cannot me zipped (not the same shape)')


class Node(BTree):
	"""
	An extension of BTree. 
	A class used to represent a Node in a Binary Tree

	...
	
	Attributes
	----------
	value:
		A value describing the current node
	left:
		The left-subtree of the current node
	right:
		The right-subtree of the current node

	Methods
	-------
	is_node()
		Indicates if the BTree is a node   
	get_value()
		Get the value contained in the node
	set_value(v)
		Set the value contained in the node
	get_left()
		Get the left subtree of the current node 
	get_right()
		Get the right subtree of the current node 
	map(kl, kn)
		Applies kl to every leaf values of the Btree, and kn to every node values
	mapt(kl, kn)
		Applies kl to every leaf values the current instance, and kn to every subtrees that are nodes
	reduce(k)
		Reduces a BTree into a single value using k
	uacc(k)
		Makes an upward accumulation of the values in a BTree using k
	dacc(gl, gr, c)
		Makes an downward accumulation of the values in a BTree using gl, gr and c
	zip(t)
		Zip the values contained in t with the ones in the current instance
	"""
	def __init__(self, value, left, right):
		self.value = value
		self.left = left
		self.right = right

	def __str__(self):
		return "node " +  str(self.value) +" (" + str(self.left) + ") (" + str(self.right) + ")"

	def is_node(self):
		return True

	def set_value(self, param):
		self.value = param

	def get_value(self):
		return self.value

	def get_right(self):
		return self.right

	def get_left(self):
		return self.left

	def map(self, kl, kn):
		"""
		Applies kl to every leaf values of the current instance, and kn to every node values

		Parameters
		----------
		kl : lambda x => y
			The function to apply to every leaf values of the current instance
		kn : lambda x => y
			The function to apply to every node values of the current instance
		"""
		new_val = kn(self.get_value())
		left = self.get_left().map(kl, kn)
		right = self.get_right().map(kl, kn)
		return Node(new_val, left, right)

	def mapt(self, kl, kn):
		"""
		Applies kl to every leaf values the current instance, and kn to every subtrees that are nodes

		Parameters
		----------
		kl : lambda x => y
			The function to apply to every leaf values of the current instance
		kn : lambda x y z => r
			The function to apply to every node subtrees of the current instance
		"""
		new_val = kn(self.get_value(), self.get_left(), self.get_right())
		left = self.get_left().mapt(kl, kn)
		right = self.get_right().mapt(kl, kn)
		return Node(new_val, left, right)

	def reduce(self, k):
		"""
		Reduces a BTree into a single value using k

		We use recursive calls of sub-reduction to make a total reduction.
		
		Parameters
		----------
		k : lambda x y z => r
			The function used to reduce a BTree into a single value 
		"""
		left = self.get_left().reduce(k)
		right = self.get_right().reduce(k)
		return k(left, self.get_value(), right)

	def uacc(self, k):
		"""
		Makes an upward accumulation of the values in the current instance using k

		Every values in nodes are replaced by the reduced value of the BTree considering the current node as the root.

		Parameters
		----------
		k : lambda x y z => r
			The function used to reduce a BTree into a single value 
		"""
		r = self.reduce(k)
		return Node(r, self.get_left().uacc(k), self.get_right().uacc(k))

	def dacc(self, gl, gr, c):
		"""
		Makes an downward accumulation of the values in a BTree using gl, gr and c

		Parameters
		----------
		gl : lambda x y => z
			Function to make an accumulation to the left part of a node
		gr : lambda x y => z
			Function to make an accumulation to the right part of a node
		c : 
			Accumulator for the downward computation
		"""
		a = self.get_value()
		left = self.get_left().dacc(gl, gr, gl(c, a))
		right = self.get_right().dacc(gl, gr, gr(c, a))
		return Node(k, self.get_left().uacc(k),  self.get_right().uacc(k))

	def zip(self, t):
		"""
		Zip the values contained in t with the ones in the current instance

		Parameters
		----------
		t : BTree
			The BTree to zip with the current instance

		Raises
		------
		NotEqualSizeError
			If the type of t is not the same one than the current instance
		"""
		if t.is_node():
			v = (self.get_value(), t.get_value())
			left = self.get_left().zip(t.get_left())
			right = self.get_right().zip(t.get_right())
			return Node(v, left, right)
		else:
			raise NotEqualSizeError('The two types of BTree cannot me zipped (not the same shape)')