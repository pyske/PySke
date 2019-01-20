from pyske.errors import NotEqualSizeError
from pyske.slist import SList

class RNode:
	"""
	TODO
	"""

	def __init__(self, value, ts = SList()):
		self.value = value
		self.childrens = ts


	def __str__(self):
		res = "rnode " + str(self.value) + "["
		ch = self.get_childrens()
		for i in range(0, self.get_childrens().length()):
			if i == ch.length() - 1:
				res = res + str(ch[i]) 
			else:
				res = res + str(ch[i]) + ", " 
		return res + "]"


	def __eq__(self, other):
		if isinstance(other, RNode):
			ch1 = self.get_childrens()
			ch2 = other.get_childrens()
			if ch1.length() != ch2.length():
				return False
			for i in range(0, ch1.length()):
				if ch1[i] != ch2[i]:
					return False
			return (self.get_value() == other.get_value())
		return False


	def get_childrens(self):
		return self.childrens


	def add_children(self, c):
		self.childrens.append(c)


	def get_value(self):
		return self.value


	def set_value(self, v):
		self.value = v


	def map(self, f):
		"""
		TODO documentation
		"""
		v = f(self.get_value())
		#To each element of the list of children, we apply the RNode.map function 
		ch = self.get_childrens().map(lambda x: x.map(f)) 
		return RNode(v, ch)


	def reduce(self, f, g):
		"""
		TODO documentation
		"""
		if self.get_childrens.empty():
			return self.get_value()
		# We calculate the reduction of each childen
		reductions = self.get_childrens().map(lambda x: x.reduce(f, g)) 
		# We combine every sub reductions using g
		red = reductions[0]
		for i in range(1, reductions.length()):
			red = g(red, reductions[i])
		# The final reduction is the result of the combination of sub reductions and the value of the current instance
		return f(self.get_value(), red)


	def uacc(self, f, g):
		"""
		TODO documentation
		"""
		v = self.reduce(f, g)
		ch = self.get_childrens().map(lambda x: x.uacc(f, g))
		return RNode(v, ch)


	def dacc(self, f, unit_f):
		"""
		TODO documentation
		"""
		def dacc2(self, f, c):
			"""
			TODO documentation
			"""
			a = self.get_value()
			ch = self.get_childrens().map(lambda x: x.dacc2(f, f(c,a)))
			return RNode(c, ch)
		return self.dacc2(f, unit_f)


	def zip(self, rt):
		"""
		TODO documentation
		"""
		ch1 = self.get_childrens()
		ch2 = rt.get_childrens()
		if ch1.length() != ch2.length():
			raise NotEqualSizeError("The rose trees cannot be zipped (not the same shape)")
		ch = []
		for i in range(0, ch1.length()):
			ch.append(ch1[i].zip(ch2))
		v = (self.get_value(), rt.get_value())
		return RNode(v, ch)


	def zipwith(self, rt, f):
		"""
		TODO documentation
		"""
		ch1 = self.get_childrens()
		ch2 = rt.get_childrens()
		if ch1.length() != ch2.length():
			raise NotEqualSizeError("The rose trees cannot be zipped (not the same shape)")
		ch = []
		for i in range(0, ch1.length()):
			ch.append(ch1[i].zip(ch2, f))
		v = f(self.get_value(), rt.get_value())
		return RNode(v, ch)


	def racc(self, f, unit_f):
		"""
		TODO documentation
		"""
		# TODO test to check if it does match its specification:
		# rAcc (+) (RNode a ts)
		#	= let rs = scan (+) [root ts[i] | i in [1 .. #ts]]
		#	in  RNode unit_(+) [setroot (rAcc (+) ts[i]) r[i] | i in [1 .. #ts]]
		rv = self.get_childrens().map(lambda x: x.get_value())
		rs = rv.scan(f, unit_f)
		ch = []
		ch0 = self.get_childrens()
		for i in range(0, ch0.length()):
			c = ch0[i]
			cs = c.racc(f, unit_f)
			cs.set_value(rs[i])
			ch.append(cs)
		return RNode(unit_f, ch)


	def lacc(self, f, unit_f):
		"""
		TODO documentation
		"""
		# TODO test to check if it does match its specification:
		# lAcc (+) (RNode a ts)
		#	= let rs = scan2 (+) [root ts[i] | i in [1 .. #ts]]
		#	in  RNode unit_(+) [setroot (lAcc (+) ts[i]) r[i] | i in [1 .. #ts]]
		rv = self.get_childrens().map(lambda x: x.get_value())
		rs = rv.scan2(f, unit_f)
		ch = [] # TODO
		ch0 = self.get_childrens()
		for i in range(0, ch0.length()):
			c = ch0[i]
			cs = c.lacc(f, unit_f)
			cs.set_value(rs[i])
			ch.append(cs)
		return RNode(unit_f, ch)

