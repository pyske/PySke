from enum import Enum
from pyske.errors import NotEqualSizeError, UnknownTypeError
from pyske.slist import SList

class VTag(Enum):
	LEAF = "L", 'tag used represent a leaf in a linearized tree'
	NODE = "N", 'tag used represent a node in a linearized tree'
	CRITICAL = "C", 'tag used represent a critical node in a linearized tree'

	def __str__(self):
		return self.value[0]


def parseVTag(vt):
	"""
	Get a VTag from a label

	Parameters
	----------
	t : str
		A label that we want to get the VTag
	
	Raises
	------
	UnknownTypeError
		If the label is not known in VTag
	"""
	for t in VTag:
		if t.value[0] == vt:
			return t
	raise UnknownTypeError('Type of value unknown: '+str(vt))


class TaggedValue:
	"""
	A class used to represent a Value in a linearized tree

	...
	
	Attributes
	----------
	val:
		A value describing the current element
	type: VTag

	Methods
	-------
	getVTag()
		Get the VTag value used to describe the tag of the current instance
	getVTagEnum()
		Get the VTag tag of the current instance
	getValue()
		Get the value contained in the current instance
	isLeaf()
		Indicates if the current instance is tagged by the Leaf VTag
	isCritical()
		Indicates if the current instance is tagged by the Critical VTag
	isNode()
		Indicates if the current instance is tagged by the Node VTag
	"""
	def __init__(self, val, t):
		self.val = val
		if (t == VTag.LEAF) | (t == VTag.NODE) | (t == VTag.CRITICAL):
			self.tag = t 
		else:
			try:
				self.tag=parseVTag(t)
			except UnknownTypeError as e:
				print(str(e))


	def __str__(self):
		return "("+str(self.val)+"^"+str(self.tag)+")"


	def __eq__(self, other):
		if isinstance(other, TaggedValue):
			return (self.tag == other.tag) and (self.val == other.val)
		return False


	def get_tag(self):
		return self.tag


	def get_value(self):
		return self.val


	def is_leaf(self):
		return self.tag == VTag.LEAF


	def is_critical(self):
		return self.tag == VTag.CRITICAL    


	def is_node(self):
		return self.tag == VTag.NODE


class Segment(SList):
	"""
	A list of TaggedValue
	TODO documentation
	"""

	def __eq__(self, other):
		if isinstance(other, Segment):
			if self.length() != other.length():
				return False
			for i in range(0, self.length()):
				if self[i] != other[i]:
					return False
			return True
		return False


	def __str__(self):
		res = "["
		for i in range(0, self.length()):
			res = res + str(self[i])
			if i != self.length() - 1:
				res = res + ", "
		return res + "]"


	def has_critical(self):
		for v in self:
			if v.get_vtype() == VTag.CRITICAL:
				return True
		return False


class LTree(SList):
	"""
	A list of Segment
	TODO documentation
	"""

	# TODO Create a constructor which takes a bt as a parameter

	def __eq__(self, other):
		if isinstance(other, LTree):
			if self.length() != other.length():
				return False
			for i in range(0, self.length()):
				if self[i] != other[i]:
					return False
			return True
		return False


	def __str__(self):
		res = "["
		for i in range(0, self.length()):
			res = res + str(self[i])
			if i != self.length() - 1:
				res = res + ", "
		return res + "]"


	def nb_values(self):
		"""
		Count the total number of value contained in the current instance
		"""
		n = 0
		for seg in self:
			n = n + seg.length()
		return n


	def replace_values(self, l):
		"""
		Replace all the values contained in a linearized tree by a list of new value

		Parameters
		----------
		l : list
			A list of new value

		Raises
		------
		AssertionError
			If there is not enough value in l to replace
		"""
		if len(l) != self.nb_values():
			raise NotEqualSizeError("The number of replacing values is not equal to the number of values in the current instance (" + str(len(l)) +" vs " + str(self.nb_values()) + ")")
		res = LTree()
		for seg in self:
			res_seg = Segment()
			for i in range(0,seg.length()):
				res_seg.append(TaggedValue(l.pop(), seg[i].get_tag()))
			res.append(res_seg)
		return res
