import sys
from enum import Enum
from pyske.errors import NotEqualSizeError, UnknownTypeError, IllFormedError, ApplicationError
from pyske.slist import SList
from pyske.btree import BTree

MINUS_INFINITY = -sys.maxsize - 1

class VTag(Enum):
	LEAF = "L" #'tag used represent a leaf in a linearized tree'
	NODE = "N" #'tag used represent a node in a linearized tree'
	CRITICAL = "C" #'tag used represent a critical node in a linearized tree'

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
	is_leaf()
		Indicates if the current instance is tagged by the Leaf VTag
	is_critical()
		Indicates if the current instance is tagged by the Critical VTag
	is_node()
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
		"""
		Get the VTag value used to describe the tag of the current instance
		"""
		return self.tag


	def get_value(self):
		"""
		Get the VTag tag of the current instance
		"""
		return self.val


	def is_leaf(self):
		"""
		Indicates if the current instance is tagged by the Leaf VTag
		"""
		return self.tag == VTag.LEAF


	def is_critical(self):
		"""
		Indicates if the current instance is tagged by the Critical VTag
		"""
		return self.tag == VTag.CRITICAL    


	def is_node(self):
		"""
		Indicates if the current instance is tagged by the Node VTag
		"""
		return self.tag == VTag.NODE


class Segment(SList):
	"""
	A list of TaggedValue
	
	Methods
	-------
	has_critical()
		Indicates if the current instance contains a value tagged by the Critical VTag
	map_local(kl, kn)
		TODO
	reduce_local(k, phi, psi_l, psi_r)
		TODO
	reduce_global(psi_n)
		TODO
	uacc_local(k, phi, psi_l, psi_r)
		TODO
	uacc_global(psi_n)
		TODO
	uacc_update(seg, k, lc, rc)
		TODO
	dacc_path(phi_l, phi_r, psi_u)
		TODO
	dacc_global(psi_d, c)
		TODO
	dacc_local(gl, gr, c)
		TODO
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
		"""
		Indicates if the current instance contains a value tagged by the Critical VTag
		"""
		for v in self:
			if v.is_critical():
				return True
		return False


	def map_local(self, kl, kn):
		"""
		TODO
		"""
		res = Segment()
		for tv in self:
			if tv.is_leaf():
				v = TaggedValue(kl(v.get_value()), v.get_tag())
			else: # v.is_node() or v.is_critical()
				v = TaggedValue(kn(v.get_value()), v.get_tag())
			res.append(v)
		return res


	def reduce_local(self, k, phi, psi_l, psi_r):
		"""
		TODO
		"""
		if self.empty():
			raise IllFormedError("reduce_local cannot be applied to an empty segments")
		stack = []
		d = MINUS_INFINITY
		has_critical = False
		for v in self.reverse():
			if v.is_leaf():
				stack.append(v.get_value())
				d = d+1
			elif v.is_node():
				if len(stack) < 2:
					raise IllFormedError("reduce_local cannot be applied to a ill-formed segment")
				lv = stack.pop()
				rv = stack.pop()
				if d == 0:
					stack.append(psi_l(lv, phi(v.get_value()), rv))
				elif d == 1:
					stack.append(psi_r(lv, phi(v.get_value()), rv))
					d = 0
				else :
					stack.append(k(lv, v.get_value(), rv))
			else: #v.is_critical()
				stack.append(phi(v.get_value()))
				has_critical = True
				d = 0
		top = stack.pop()
		if has_critical:
			return TaggedValue(top,"N")
		else:
			return TaggedValue(top,"L")


	def reduce_global(self, psi_n):
		"""
		TODO
		"""
		if self.has_critical():
			raise IllFormedError("reduce_global cannot be applied to a segments which contains a critical")
		if self.empty():
			raise IllFormedError("reduce_global cannot be applied to an empty global segment")
		stack = []
		for g in self.reverse():
			if g.is_leaf():
				stack.append(g.get_value())
			else : #g.is_node()
				if len(stack) < 2:
					raise IllFormedError("reduce_global cannot be applied to ill-formed reduced segments")
				lv = stack.pop()
				rv = stack.pop()
				stack.append(psi_n(lv, g.get_value(), rv))
		top = stack.pop()
		return top


	def uacc_local(self, k, phi, psi_l, psi_r):
		"""
		TODO
		"""
		stack = []
		d = MINUS_INFINITY
		res = Segment()
		for v in self.reverse():

			if v.is_leaf():
				res.insert(0, v)
				stack.append(v.get_value())
				d = d+1

			elif v.is_node():
				if len(stack) < 2:
					raise IllFormedError("uacc_local cannot be applied to a ill-formed segment")
				lv = stack.pop()
				rv = stack.pop()
				if d == 0:
					stack.append(psi_l(lv, phi(v.get_value()), rv))
					res.insert(0, v)
				elif d == 1:
					stack.append(psi_r(lv, phi(v.get_value()), rv))
					res.insert(0, v)
					d = 0
				else :
					val = k(lv, v.get_value(), rv)
					res.insert(0, TaggedValue(val, v.get_tag()))
					stack.append(val)
					d = d-1

			else: #v.is_critical()
				stack.append(phi(v.get_value()))
				res.insert(0,v)
				d = 0

		top = stack.pop()
		return (top, res)


	def uacc_global(self, psi_n):
		"""
		TODO
		"""
		stack = []
		res = Segment()
		if self.has_critical():
			raise IllFormedError("uacc_global cannot be applied to a segments which contains a critical")
		if self.empty():
			raise IllFormedError("uacc_global cannot be applied to an empty global segment")
		for g in self.reverse():
			if g.is_leaf():
				res.insert(0, g)
			else: # g.is_node()
				if len(stack) < 2:
					raise IllFormedError("uacc_global cannot be applied to ill-formed segment of accumulation")
				lv = stack.pop()
				rv = stack.pop()
				val = psi_n(lv, g.get_value(), rv)
				res.insert(0, TaggedValue(val, g.get_tag()))
		return res


	def uacc_update(self, seg, k, lc, rc):
		"""
		TODO
		"""
		stack = [rc.get_value(), lc.get_value()]
		d = MINUS_INFINITY
		res = Segment()
		for i in range(seg.length() - 1, -1, -1):
			v1 = self[i]
			v2 = seg[i]
			if v1.is_leaf():
				res.append(v2)
				stack.append(v2.get_value())
				d = d+1
			elif v1.is_node():
				if len(stack) < 2:
					raise IllFormedError("uacc_update cannot be applied to ill-formed segments")
				lv = stack.pop()
				rv = stack.pop()
				if d == 0 | d == 1:
					val = k(lv, v1.get_value(), rv)
					res.append(TaggedValue(val, v1.get_tag()))
					stack.append(val)
					d = 0
				else:
					res.append(v2)
					stack.append(v2.get_value())
					d = d-1
			else: #v1.is_critical()
				if len(stack) < 2:
					raise IllFormedError("uacc_update cannot be applied to ill-formed segments")
				lv = stack.pop()
				rv = stack.pop()
				val = k(lv, v1.get_value(), rv)
				res.append(TaggedValue(val, v1.get_tag()))
				stack.append(val)
				d = 0
		return res


	def dacc_path(self, phi_l, phi_r, psi_u):
		"""
		TODO
		"""
		d = MINUS_INFINITY
		to_l = None
		to_r = None
		has_critical = False
		for v in self.reverse():
			if v.is_leaf():
				d = d+1
			elif v.is_node():
				if d == 0:
					if to_l == None | to_r == None:
						raise IllFormedError("dacc_path cannot be applied to a ill-formed segment")
					to_l = psi_u(phi_l(v.get_value()), to_l)
					to_r = psi_u(phi_l(v.get_value()), to_r)
				elif d == 1:
					if to_l == None | to_r == None:
						raise IllFormedError("dacc_path cannot be applied to a ill-formed segment")
					to_l = psi_u(phi_l(v.get_value()), to_l)
					to_r = psi_u(phi_l(v.get_value()), to_r)
				else: 
					d = d-1
			else : #v.is_critical()
				has_critical = True
				to_l = phi_l(v.get_value())
				to_r = phi_r(v.get_value())
				d = 0
		if not has_critical:
			raise ApplicationError("dacc_path must be imperatively applied to a segment which contains a critical node")
		return TaggedValue((to_l, to_r), "N")


	def dacc_global(self, psi_d, c):
		"""
		TODO
		"""
		stack = [c]
		res = Segment()
		if self.has_critical():
			raise IllFormedError("dacc_global cannot be applied to segment which contains a critical node")
		for v in self:
			if len(stack) == 0 :
				raise IllFormedError("dacc_global cannot be applied to ill-formed segments")
			val = stack.pop()
			res.append(TaggedValue(val, v.get_tag()))
			if v.is_node():
				(to_l, to_r) = v.get_value()
				stack.append(psi_d(v, to_r))
				stack.append(psi_d(v, to_l))
		return res


	def dacc_local(self, gl, gr, c):
		"""
		TODO
		"""
		stack = [c]
		res = Segment()
		for v in self:
			if v.is_leaf() | v.is_critical():
				if len(stack) == 0 :
					raise IllFormedError("dacc_local cannot be applied to a ill-formed segment")
				val = stack.pop()
				res.append(TaggedValue(val, v.get_tag()))
			else : #v.is_node()
				if len(stack) == 0 :
					raise IllFormedError("dacc_local cannot be applied to a ill-formed segment")
				val = stack.pop()
				res.append(TaggedValue(val, v.get_tag()))
				stack.append(gr(val, v.get_value()))
				stack.append(gl(val, v.get_value()))
		return res


class LTree(SList):
	"""
	A list of Segment
	
	Methods
	-------
	nb_values()
		Counts the total number of value contained in the current instance
	replace_values(l)
		Replaces all the values contained in a linearized tree by a list of new values
	map(kl, kn)
		TODO
	reduce(k, phi, psi_n, psi_l, psi_r)
		TODO
	uacc(k, phi, psi_n, psi_l, psi_r)
		TODO
	dacc(gl, gr, c, phi_l, phi_r, psi_u, psi_d)
		TODO
	"""

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
		Counts the total number of value contained in the current instance
		"""
		n = 0
		for seg in self:
			n = n + seg.length()
		return n


	def replace_values(self, l):
		"""
		Replaces all the values contained in a linearized tree by a list of new values

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


	def map(self, kl, kn):
		"""
		TODO
		"""
		res = LTree()
		for seg in self:
			res.append(seg.map_local(kl,kn))
		return res


	def reduce(self, k, phi, psi_n, psi_l, psi_r):
		"""
		TODO
		"""
		tops = Segment()
		for seg in self:
			tops.append(seg.reduce_local(k, phi, psi_l, psi_r))
		return tops.reduce_global(psi_n)


	def uacc(self, k, phi, psi_n, psi_l, psi_r):
		"""
		TODO
		"""
		gt = Segment()
		lt2 = LTree()
		for seg in self:
			(top, res) = seg.uacc_local(k, phi, psi_l, psi_r)
			gt.append(top)
			lt2.append(res)
		gt2 = gt.uacc_global(psi_n)
		res = Segment()
		for i in range(0, gt.length()):
			if gt[i].is_node():
				seg_res = self[i].uacc_update(k, lt2[i], gt2[i])
				res.append(seg_res)
			else:
				res.append(lt2[i])
		return res


	def dacc(self, gl, gr, c, phi_l, phi_r, psi_u, psi_d):
		"""
		TODO
		"""
		gt = Segment()
		res = LTree()
		for seg in self:
			if seg.has_critical():
				gt.append(seg.dacc_path(phi_l, phi_r, psi_u))
			else:
				v = seg[0]
				gt.append(TaggedValue(v.get_value(), "L"))

		gt2 = gt.dacc_global(psi_d, c)

		for i in range(0, gt.length()):
			res.append(self[i].dacc_local(gl, gr, gt2[i].get_value()))
		return res


def __tv2lv(bt_val):
	val = bt_val.get_value()
	res = Segment()
	res_0 = Segment()
	if bt_val.is_leaf():
		res_0.append(val)
		res.append(res_0)
	else: #bt_val.is_node()
		res_left = Segment(__tv2lv(bt_val.get_left()))
		res_right = Segment(__tv2lv(bt_val.get_right()))
		if val.is_critical():
			res_0.append(val)
			res.append(res_0)
			res.extend(res_left)
			res.extend(res_right)
		else: # val.is_node()
			res_0.append(val)
			res_0.extend(res_left[0])
			res_0.extend(res_right[0])
			res.append(res_0)
			res.extend(res_left[1:])
			res.extend(res_right[1:])
	return res


def serialization(bt, m):
	# Get a LTree from a BTree
	up_div = lambda n,m: (int(n / m) + (0 if n % m == 0 else 1))
	bt_one = bt.map(lambda x : 1, lambda x : 1)
	bt_size = bt_one.uacc(lambda x,y,z : x+y+z)
	bt_tags = bt_size.mapt(lambda x: VTag.LEAF, 
		lambda x, y, z: VTag.CRITICAL if up_div(x,m) > up_div(y.get_value(),m) and up_div(x,m) > up_div(z.get_value(),m) else VTag.NODE)
	bt_val = bt.zipwith(bt_tags, lambda x,y: TaggedValue(x,y))
	return LTree(__tv2lv(bt_val))

#TODO deserialization
