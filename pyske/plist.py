from pyske.slist import SList
from mpi4py import MPI
from pyske.support.parallel import *

class PList:

	def __init__(self):
		self.__content = []
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
		p.__start_index = SList(p.__distribution).scan(lambda x,y:x+y,0)[pid]
		p.__content = [f(i) for i in range(p.__start_index, p.__start_index + p.__local_size)]
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
		p.__content = SList(self.__content).reduce(lambda x,y: x+y, [])
		p.__local_size = len(p.__content)
		p.__distribution = comm.allgather(p.__local_size)
		p.__start_index = SList(p.__distribution).scan(lambda x, y: x + y, 0)[pid]
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


	def __str__(self):
		return "pid["+str(pid)+"]:\n" + \
			   "  global_size: "+ str(self.__global_size)+ "\n" + \
			   "  local_size: " + str(self.__local_size) + "\n" + \
			   "  start_index: " + str(self.__start_index) + "\n" + \
			   "  distribution: " + str(self.__distribution) + "\n" + \
			   "  content: " + str(self.__content) +"\n"

	# TODO implement skeletons primitives (map_local, etc) for a list
	# Communication ?