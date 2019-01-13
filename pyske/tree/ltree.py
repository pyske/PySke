from enum import Enum

class VType(Enum):
	LEAF = "L", 'tag used represent a leaf in a linearized tree'
	NODE = "N", 'tag used represent a node in a linearized tree'
	CRITICAL = "C", 'tag used represent a critical node in a linearized tree'


def parseVType(vt):
	"""
	Get a VType from a label

	Parameters
	----------
	t : str
		A label that we want to get the VType
	
	Raises
	------
	Exception
		If the label is not known in VType
	"""
	for t in VType:
		if t.value == vt:
			return t
	raise Exception('type of value unknown: '+str(t))


class Value:
	"""
	A class used to represent a Value in a linearized tree

	...
	
	Attributes
	----------
	val:
		A value describing the current element
	type: VType

	Methods
	-------
	getVType()
		Get the VType value used to describe the tag of the current instance
	getVTypeEnum()
		Get the VType tag of the current instance
	getValue()
		Get the value contained in the current instance
	isLeaf()
		Indicates if the current instance is tagged by the Leaf VType
	isCritical()
		Indicates if the current instance is tagged by the Critical VType
	isNode()
		Indicates if the current instance is tagged by the Node VType
	"""
	def __init__(self, val, t):
		self.val = val
		if (t == VType.LEAF) | (t == VType.NODE) | (t == VType.CRITICAL):
			self.type = t 
		else:
			self.type=parseVType(t)

	def __str__(self):
		return "("+str(self.val)+"^"+self.getVType()+")"

	def __eq__(self, other):
		if isinstance(other, Value):
			return (self.getVType() == other.getVType()) and (self.getValue() == other.getValue())
		return False

	def getVType(self):
		return self.type.value

	def getVTypeEnum(self):
		return self.type

	def getValue(self):
		return self.val

	def isLeaf(self):
		return self.type == VType.LEAF

	def isCritical(self):
		return self.type == VType.CRITICAL    

	def isNode(self):
		return self.type == VType.NODE


def nbValue(ltree):
	"""
	Count the total number of value contained in a linearized tree

	Parameters
	----------
	ltree : [[Value]]
		The linearized tree that we want to count the number of element
	"""
	n = 0
	for seg in ltree:
		n + len(seg)
	return n


def replaceValues(ltree, l):
	"""
	Replace all the values contained in a linearized tree by a list of new value

	Parameters
	----------
	ltree : [[Value]]
		The linearized tree that we want to change the values
	l : list
		A list of new value

	Raises
	------
	AssertionError
		If there is not enough value in l to replace
	"""
	assert len(l) < nbValues(ltree)
	for seg in ltree:
		for i in range(0,len(seg)):
			new_val = Value(l.pop(), seg[i].getVType())
			seg[i] = new_val


def eq_seg(s1, s2):
	"""
	Test the equality of two segment of a linearized tree

	Parameters
	----------
	s1 : [Value]
		The first list of Value to compare
	s2 : [Value]
		The second list of Value to compare
	"""
	if len(s1) != len (s2):
		return False
	for i in range(0, len(s1)):
		if s1[i] != s2[i]:
			return False
	return True


def eq_ltree(lt1, lt2):
	"""
	Test the equality of two linearized tree

	Parameters
	----------
	lt1 : [[Value]]
		The first linearized tree to compare
	lt2 : [[Value]]
		The second linearized tree to compare
	"""
	if len(lt1) != len (lt2):
		return False
		for i in range(0, len(lt1)):
			if not eq_seg(lt1[i], lt2[i]):
				return False
	return True