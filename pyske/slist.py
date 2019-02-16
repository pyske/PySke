import functools
from pyske.errors import NotEqualSizeError, EmptyError


LEFT_LIST = "["
RIGHT_LIST = "]"
SEPARATOR_LIST = ";"

class SList(list):
	"""
	An extended definition of lists, including Bird-Meertens Formalism primitives

	...

	Methods
	-------
	head()
		Gives the first element of the current instance
	tail()
		Gives the the current instance without its first element 
	length()
		Gives the number of element in the current instance
	filter(f)
		Removes all the elements that don't verify a predicate
	empty()
		Indicates if a list is empty
	reverse()
		Reverse a list
	map(f)
		Applies f to every element of the current instance
	reduce(f)
		Reduce the current instance using a reduction function
	scan(f, c)
		Makes an rightward accumulation of the element on the current instance from an initial value
	scan2(f)
		Makes an rightward accumulation of the element on the current instance from an initial value
	zip(l)
		Creates a list of pairs from the element of the current instance and another one
	zipwith(l, f)
		Creates a list of new elements using a function from the element of the current instance and another one
	"""


	def __str__(self):
		res = LEFT_LIST
		for i in range(0, self.length()):
			res = res + str(self[i])
			if i != self.length() - 1:
				res = res + SEPARATOR_LIST + " "
		return res + RIGHT_LIST


	def from_str(s, parser = int):
		res = SList([])
		s=s.replace(LEFT_LIST, "")
		s=s.replace(RIGHT_LIST, "")
		values = s.split(SEPARATOR_LIST)
		for v in values:
			res.append(parser(v))
		return res


	def head(self):
		"""
		Gives the first element of the current instance
		"""
		if self.is_empty():
			return None
		else:
			return self[0]

	def tail(self):
		"""
		Gives the the current instance without its first element 
		"""
		return SList(self[1:])


	def length(self):
		"""
		Gives the number of element in the current instance
		"""
		return len(self)


	def filter(self, p):
		"""
		Removes all the elements that don't verify a predicate

		Parameters
		----------
		p : predicate (x => bool)
			A predicate that all elements in the result must verify 
		"""
		return SList(filter(p,self))


	def is_empty(self):
		"""
		Indicates if a list is empty
		"""
		return self.length() == 0


	def reverse(self):
		"""
		Reverse a list
		"""
		rev = SList()
		for i in range(self.length()-1, -1 , -1):
			rev.append(self[i])
		return rev


	def map(self, f):
		"""
		Applies f to every element of the current instance

		BMF definition: 
		map f [x1, x2, ..., xn] = [f(x1), f(x2), ..., f(xn)] 
		
		Parameters
		----------
		f : lambda x => y
			The function to apply to every values of the current instance
		"""
		return SList(map(f, self))


	def reduce(self, f, e=None):
		"""
		Reduce the current instance using a reduction function

		BMF definition:
		reduce f [x1, x2, ..., xn] e = f(f(f(e, x1), ...), xn)

		Parameters
		----------
		f : lambda x,y => z
			The used function to reduce the current instance
		"""
		if e is None:
			return functools.reduce(f, self)
		else:
			return functools.reduce(f, self, e)


	def scan(self, f, c):
		"""
		Makes an rightward accumulation of the element on the current instance from an initial value

		BMF definition:
		scan f c [x1, x2, ..., xn] = [c, f(c, x1), f(f(c, x1), x2), ..., f(f(...,f(f(c, x1), x2)), xn)]

		Parameters
		----------
		f : lambda x,y => z
			A function to make a new accumulation from the previous accumulation and a current value
		c :
			Initial value for the accumulator
		"""
		res = SList()
		if self.is_empty():
			res.append(c)
			return res
		else:
			res.append(c)
			for i in range(0, self.length()-1):
				c = f(c, self[i])
				res.append(c)
			return res

	def scanr(self, op):
		len = self.length()
		res = SList(range(0, len))
		if 0<len: res[0]=self[0]
		for i in range(0,len-1):
			res[i+1]=op(res[i],self[i+1])
		return res

	def scanl(self, op, e):
		len = self.length()
		res = SList(range(0, len))
		if 0<len: res[0]=e
		for i in range(0,len-1):
			res[i+1]=op(res[i],self[i])
		return res

	def scanl_last(self, op, e):
		len = self.length()
		res = SList(range(0, len))
		if 0<len: res[0]=e
		for i in range(0,len-1):
			res[i+1]=op(res[i],self[i])
		if 0<len:
			last = op(res[len-1], self[len-1])
		else:
			last = e
		return (res, last)

	def rscan(self, f, c):
		"""
		Makes an leftward accumulation of the element on the current instance from an initial value

		BMF definition:
		scan2 f [x1, x2, ..., xn] = [f(x2, f(x3 , f(..., xn)), f(x3 , f(..., xn)), ..., xn, c]

		Parameters
		----------
		f : lambda x,y => z
			A function to make a new accumulation from the previous accumulation and a current value
		c :
			Initial value for the accumulator
		"""
		res = SList()
		res.append(c)
		if self.is_empty():
			return res
		else:
			for i in range(self.length()-1, 0, -1):
				c = f(self[i], c)
				res.append(c)
			return res.reverse()


	def zip(self, l):
		"""
		Creates a list of pairs from the element of the current instance and another one

		Parameters
		----------
		l : list
			A list to merge the values of the current instance with

		Raises
		-----
		NotEqualSizeError
			If the current instance doesn't have the same number than the input
		"""
		if l.length() != self.length():
			raise NotEqualSizeError("The lists cannot be zipped (not the same size)")
		res = SList()
		for i in range(0, self.length()):
			res.append((self[i],l[i]))
		return res


	def zipwith(self, l, f):
		"""
		Creates a list of new elements using a function from the element of the current instance and another one

		Parameters
		----------
		l : list
			A list to merge the values of the current instance with
		f : lambda x, y => z
			A function to zip the values

		Raises
		-----
		NotEqualSizeError
			If the current instance doesn't have the same number than the input
		"""
		if l.length() != self.length():
			raise NotEqualSizeError("The lists cannot be zipped (not the same size)")
		res = SList()
		for i in range(0, self.length()):
			res.append(f(self[i],l[i]))
		return res
