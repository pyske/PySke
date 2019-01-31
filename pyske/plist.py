from pyske.slist import SList
from mpi4py import MPI
from pyske.support.parallel import *

class PList:

	def __init__(self):
		self.__content = []
		self.__global_size = 0
		self.__local_size = 0
		self.__start_index = 0
		self.__distribution = [0 for i in range(1, nprocs)]

	def length(self):
		return self.__global_size

	def init(f, size):
		assert(size >= 0)
		p = PList()
		p.__global_size = size
		p.__local_size = local_size(size)
		p.__start_index = 0 if pid == 0 else local_size(pid - 1, size)
		p.__content = [f(i) for i in range(p.__start_index, p.__start_index + p.__local_size)]
		p.__distribution = [local_size(i, size) for i in range(0, nprocs - 1)]
		return p

	def map(self, f):
		return PList.init(lambda i: f(self.__content[i]), self.__global_size)

	def mapi(self, f):
		return PList.init(lambda i: f(i+self.__start_index, self.__content[i]), self.__global_size)

	def map2(self, f, pl):
		assert (self.__global_size == pl.__global_size)
		return PList.init(lambda i: f(self.__content[i], pl.__content[i]), self.__global_size)

	def zip(self, pl):
		return self.map2(lambda x, y : (x, y), pl)

	# TODO implement skeletons primitives (map_local, etc) for a list
	# Communication ?