from pyske.errors import NotEqualSizeError, ConstructorError
from pyske.slist import SList
from pyske.btree import Node, Leaf, BTree

class RNode:
	"""
	A class used to represent a Rose Tree (a tree with an arbitrary shape)

	...

	Methods
	-------
	get_children()
		Get the children of the current RNode
	add_children(c)
		Add a children to the ones of the current RNode
	is_leaf()
		Indicates if the current RNode has no children, and then can be considered as a leaf
	is_node()
		Indicates if the current RNode has children, and then can be considered as a node
	get_value()
		Get the value of the current RNode
	set_value(v)
		Set a new value for the current RNode
	map(f)
		Applies a function to every values contained in the current instance
	reduce(f, g)
		Reduce the current instance into a single value using two operators
	uacc(f, g)
		Makes an upward accumulation of the values in a the current instance using two operators
	dacc(f, unit_f)
		Makes an downward accumulation of the values in a the current instance
	zip(rt)
		Zip the values contained in a second RTree with the ones in the current instance
	zipwith(rt, f)
		Zip the values contained in a second RTree with the ones in the current instance using a function
	racc(f, unit_f)
		Makes a rightward accumulation of the values in the current instance
	lacc(f, unit_f)
		Makes a leftward accumulation of the values in the current instance
	r2b()
		Get a BTree from the current instance
	"""

	def __init__(self, value, ts = SList()):
		if isinstance(value, BTree):
			if value == Leaf(None):
				raise ConstructorError("A RTree cannot be constructed from a single Leaf that contains None")
			# Create a RTree from a BTree
			bt = value
			rt = RNode.b2r(bt)
			self.value = rt.get_value()
			self.children = rt.get_children()
		else:	
			self.value = value
			self.children = ts

	def b2r(bt):
		def aux(bt):
			if bt.is_leaf():
				val = bt.get_value()
				if val == None:
					return SList()
				else:
					return SList([RNode(val)])
			else:
				n = bt.get_value() 
				left = bt.get_left()
				right = bt.get_right()
				res_l = aux(left)
				res_r = aux(right)
				res_head = RNode(n, res_l) 
				res_r.insert(0, res_head)
				return res_r
		return aux(bt).head()

	def __str__(self):
		res = "rnode " + str(self.value) + "["
		ch = self.get_children()
		for i in range(0, self.get_children().length()):
			if i == ch.length() - 1:
				res = res + str(ch[i]) 
			else:
				res = res + str(ch[i]) + ", " 
		return res + "]"


	def __eq__(self, other):
		if isinstance(other, RNode):
			ch1 = self.get_children()
			ch2 = other.get_children()
			if ch1.length() != ch2.length():
				return False
			for i in range(0, ch1.length()):
				if ch1[i] != ch2[i]:
					return False
			return (self.get_value() == other.get_value())
		return False


	def is_leaf(self):
		"""
		Indicates if the current RNode has no children, and then can be considered as a leaf
		"""
		return len(self.children == 0)


	def is_node(self):
		"""
		Indicates if the current RNode has children, and then can be considered as a node
		"""
		return len(self.children != 0)


	def get_children(self):
		"""
		Get the children of the current RNode
		"""
		return self.children


	def add_children(self, c):
		"""
		Add a children to the ones of the current RNode
		
		Parameters
		----------
		c :
			The children to add
		"""
		self.children.append(c)


	def get_value(self):
		"""
		Get the value of the current RNode
		"""
		return self.value


	def set_value(self, v):
		"""
		Set a new value for the current RNode

		Parameters
		----------
		v :
			The new value to set
		"""
		self.value = v


	def map(self, f):
		"""
		Applies a function to every values contained in the current instance
		
		Parameters
		----------
		f : lambda x => y
			The function to apply to every values of the current instance
		"""
		v = f(self.get_value())
		#To each element of the list of children, we apply the RNode.map function 
		ch = self.get_children().map(lambda x: x.map(f)) 
		return RNode(v, ch)


	def reduce(self, f, g):
		"""
		Reduce the current instance into a single value using two operators

		Parameters
		----------
		f : lambda x, y => z
			A binary operator to combine all sub reduction of the children of the current instance into an intermediate reduction
		g : lambda x, y => z
			A binary operator to combine the value of the current instance with the intermediate reduction
		"""
		if self.get_children.empty():
			return self.get_value()
		# We calculate the reduction of each childen
		reductions = self.get_children().map(lambda x: x.reduce(f, g)) 
		# We combine every sub reductions using g
		red = reductions[0]
		for i in range(1, reductions.length()):
			red = g(red, reductions[i])
		# The final reduction is the result of the combination of sub reductions and the value of the current instance
		return f(self.get_value(), red)


	def uacc(self, f, g):
		"""
		Makes an upward accumulation of the values in a the current instance using two operators

		Parameters
		----------
		f : lambda x, y => z
			A binary operator to combine all top values from the accumulation within the children of the current instance into an intermediate accumulation
		g : lambda x, y => z
			A binary operator to combine the value of the current instance with the intermediate accumulation
		"""
		v = self.reduce(f, g)
		ch = self.get_children().map(lambda x: x.uacc(f, g))
		return RNode(v, ch)


	def dacc(self, f, unit_f):
		"""
		Makes an downward accumulation of the values in a the current instance
		
		Parameters
		----------
		f : lambda x, y => z
			A function to accumulate the value of the current instance with the current accumulator
		unit_f :
			A value such as, forall x, f(x, unit_f) = x
		"""
		def dacc2(self, f, c):
			# Auxiliary function to make an accumulation with an arbitrary accumulator
			a = self.get_value()
			ch = self.get_children().map(lambda x: x.dacc2(f, f(c,a)))
			return RNode(c, ch)
		# Since the accumulator changes at each iteration, we need to use a changing parameter, not defined in dacc.
		# Use of an auxiliary function, with as a first accumulator, unit_f
		return self.dacc2(f, unit_f)


	def zip(self, rt):
		"""
		Zip the values contained in a second RTree with the ones in the current instance

		Parameters
		----------
		rt : RTree
			The RTree to zip with the current instance

		Raises
		------
		NotEqualSizeError
			If the shape of rt is not the same one than the current instance
		"""
		ch1 = self.get_children()
		ch2 = rt.get_children()
		if ch1.length() != ch2.length():
			raise NotEqualSizeError("The rose trees cannot be zipped (not the same shape)")
		ch = []
		for i in range(0, ch1.length()):
			ch.append(ch1[i].zip(ch2))
		v = (self.get_value(), rt.get_value())
		return RNode(v, ch)


	def zipwith(self, rt, f):
		"""
		Zip the values contained in a second RTree with the ones in the current instance using a function

		Parameters
		----------
		rt : RTree
			The RTree to zip with the current instance
		f : lambda x, y => z
			A function to zip values
		Raises
		------
		NotEqualSizeError
			If the shape of rt is not the same one than the current instance
		"""
		ch1 = self.get_children()
		ch2 = rt.get_children()
		if ch1.length() != ch2.length():
			raise NotEqualSizeError("The rose trees cannot be zipped (not the same shape)")
		ch = []
		for i in range(0, ch1.length()):
			ch.append(ch1[i].zipwith(ch2, f))
		v = f(self.get_value(), rt.get_value())
		return RNode(v, ch)


	def racc(self, f, unit_f):
		"""
		Makes a rightward accumulation of the values in the current instance

		Parameters
		----------
		f : lambda x, y => z
			A function to accumulate the value of the current instance with the current accumulator
		unit_f :
			A value such as, forall x, f(x, unit_f) = x
		"""
		# TODO test to check if it does match its specification:
		# rAcc (+) (RNode a ts)
		#	= let rs = scan (+) [root ts[i] | i in [1 .. #ts]]
		#	in  RNode unit_(+) [setroot (rAcc (+) ts[i]) r[i] | i in [1 .. #ts]]
		rv = self.get_children().map(lambda x: x.get_value())
		rs = rv.scan(f, unit_f)
		ch = []
		ch0 = self.get_children()
		for i in range(0, ch0.length()):
			c = ch0[i]
			cs = c.racc(f, unit_f)
			cs.set_value(rs[i])
			ch.append(cs)
		return RNode(unit_f, ch)


	def lacc(self, f, unit_f):
		"""
		Makes a leftward accumulation of the values in the current instance

		Parameters
		----------
		f : lambda x, y => z
			A function to accumulate the value of the current instance with the current accumulator
		unit_f :
			A value such as, forall x, f(x, unit_f) = x
		"""
		# TODO test to check if it does match its specification:
		# lAcc (+) (RNode a ts)
		#	= let rs = scan2 (+) [root ts[i] | i in [1 .. #ts]]
		#	in  RNode unit_(+) [setroot (lAcc (+) ts[i]) r[i] | i in [1 .. #ts]]
		rv = self.get_children().map(lambda x: x.get_value())
		rs = rv.rscan(f, unit_f)
		ch = [] 
		ch0 = self.get_children()
		for i in range(0, ch0.length()):
			c = ch0[i]
			cs = c.lacc(f, unit_f)
			cs.set_value(rs[i])
			ch.append(cs)
		return RNode(unit_f, ch)


	def r2b(self):
		"""
		Get a BTree from the current instance
		"""
		def r2b1(t, ss):
			a = t.get_value()
			left = r2b2(t.get_children())
			right = r2b2(ss)
			return Node(a, left, right)

		def r2b2(ts):
			if ts.is_empty():
				return Leaf(None)
			else:
				h = ts.head()
				t = ts.tail()
				return r2b1(h, t)

		return r2b1(self, SList())

