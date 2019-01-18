import functools
from pyske.errors import NotEqualSizeError

class SList(list):
	"""
	An extended definition of lists, including Bird-Meertens Formalism primitives

	...

	Methods
	-------
	length()
		Gives the number of element in the current instance
	filter(f)
		Removes all the elements that don't verify a predicate
	empty()
		Indicates if a list is empty
	map(f)
		Applies f to every element of the current instance
	reduce(f)
		Reduce the current instance using a reduction function
	scan(f, c)
		Makes an accumulation of the element on the current instance from an initial value
	scan2(f)
		Makes an accumulation of the element on the current instance only using the contained values
	zip(l)
		Creates a list of pairs from the element of the current instance and another one
	"""

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
		p : predicate (x -> bool)
			A predicate that all elements in the result must verify 
		"""
		return SList(filter(p,self))


	def empty(self):
		"""
		Indicates if a list is empty
		"""
		return self.length() == 0


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


	def reduce(self, f):
		"""
		Reduce the current instance using a reduction function

		BMF definition:
		reduce f [x1, x2, ..., xn] = f(f(f(x1, x2), ...), xn)

		Parameters
		----------
		f : lambda x,y => z
			The used function to reduce the current instance
		"""
		return functools.reduce(f,self)


	def scan(self, f, c):
		"""
		Makes an accumulation of the element on the current instance from an initial value

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
		if self.empty():
			return res.append(c)
		else:
			res.append(c)
			for i in range(0, self.length()-1):
				c = f(c, self[i])
				res.append(c)
			return res


	def scan2(self, f):
		"""
		Makes an accumulation of the element on the current instance only using the contained values

		BMF definition:
		scan2 f [x1, x2, ..., xn] = [x1, f(x1, x2), ..., f(f(f(x1, x2),...), xn)]

		Parameters
		----------
		f : lambda x,y => z
			A function to make a new accumulation from the previous accumulation and a current value
		"""
		res = SList()
		if self.empty():
			return res
		else:
			acc = self[0]
			res.append(acc)
			for i in range(1, self.length()):
				acc = f(acc, self[i])
				res.append(acc)
			return res	

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
