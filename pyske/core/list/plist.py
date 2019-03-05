from pyske.core.list.slist import SList
from pyske.core.support.parallel import *

class PList:
	"""Distributed lists"""
	def __init__(self):
		self.__content = SList([])
		self.__global_size = 0
		self.__local_size = 0
		self.__start_index = 0
		self.__distribution = [0 for i in range(0, nprocs)]

	def length(self):
		return self.__global_size

	def init(f, size):
		assert(size >= 0)
		p = PList()
		p.__global_size = size
		p.__local_size = local_size(size)
		p.__distribution = [local_size_pid(i, size) for i in range(0, nprocs)]
		p.__start_index = SList(p.__distribution).scanl(lambda x, y: x + y, 0)[pid]
		p.__content = SList([f(i) for i in range(p.__start_index, p.__start_index + p.__local_size)])
		p.__distribution = [local_size_pid(i, size) for i in range(0, nprocs)]
		return p

	def map(self, f):
		return PList.init(lambda i: f(self.__content[i-self.__start_index]), self.__global_size)

	def mapi(self, f):
		return PList.init(lambda i: f(i, self.__content[i-self.__start_index]), self.__global_size)

	def map2(self, f, pl):
		assert (self.__distribution == pl.__distribution)
		return PList.init(lambda i: f(self.__content[i-self.__start_index], pl.__content[i-self.__start_index]), self.__global_size)

	def zip(self, pl):
		return self.map2(lambda x, y : (x, y), pl)

	def get_partition(self):
		p = PList()
		p.__content = [ self.__content ]
		p.__global_size = nprocs
		p.__local_size = 1
		p.__start_index = pid
		p.__distribution = [ 1 for i in range(0, nprocs)]
		return p

	def flatten(self):
		p = PList()
		p.__content = self.__content.reduce(lambda x,y: x+y, [])
		p.__local_size = len(p.__content)
		p.__distribution = comm.allgather(p.__local_size)
		p.__start_index = SList(p.__distribution).scanl(lambda x, y: x + y, 0)[pid]
		p.__global_size = SList(p.__distribution).reduce(lambda x, y: x+y)
		return p

	def reduce(self, op, e = None):
		if e is None:
			assert(self.__global_size >= 1)
			partial = None if self.__local_size == 0 else SList(self.__content).reduce(op)
			partials = SList(comm.allgather(partial)).filter(lambda x: x is not None)
		else:
			# assert: (op, e) form a monoid
			partial = SList(self.__content).reduce(op, e)
			partials = SList(comm.allgather(partial))
		return partials.reduce(op, e)

	def __get_shape(self):
		p = PList()
		p.__local_size = self.__local_size
		p.__global_size = self.__global_size
		p.__distribution = self.__distribution
		p.__start_index = self.__start_index
		return p


	def scanr(self, op):
		assert(self.__global_size > 0)
		p = self.__get_shape()
		partials = self.__content.scanr(op)
		last = partials[self.__local_size-1]
		acc, _ = scan(op, last)
		if pid != 0:
			for i in range(0, len(partials)):
				partials[i]=op(acc, partials[i])
		p.__content = partials
		return p

	def scanl(self, op, e):
		p = self.__get_shape()
		partials, last = self.__content.scanl_last(op, e)
		acc, _ = scan(op, last)
		if pid != 0:
			for i in range(0, len(partials)):
				partials[i] = op(acc, partials[i])
		p.__content = partials
		return p

	def scanl_last(self, op, e):
		p = self.__get_shape()
		partials, last = self.__content.scanl_last(op, e)
		acc, red = scan(op, last)
		if pid != 0:
			for i in range(0, len(partials)):
				partials[i] = op(acc, partials[i])
		p.__content = partials
		return (p, red)


	def from_seq(l):
		p = PList()
		if pid==0:
			p.__content = SList(l)
			p.__distribution = [len(l)] + [0 for i in range(1, nprocs)]
		else:
			p.__content = []
		p.__distribution = comm.bcast(p.__distribution, 0)
		p.__local_size  = p.__distribution[pid]
		p.__global_size = p.__distribution[0]
		p.__start_index = 0
		return p


	def to_seq(self):
		return self.get_partition().reduce(lambda x,y: x+y, [])


	def __str__(self):
		return "pid["+str(pid)+"]:\n" + \
			   "  global_size: "+ str(self.__global_size)+ "\n" + \
			   "  local_size: " + str(self.__local_size) + "\n" + \
			   "  start_index: " + str(self.__start_index) + "\n" + \
			   "  distribution: " + str(self.__distribution) + "\n" + \
			   "  content: " + str(self.__content) +"\n"