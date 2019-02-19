from pyske.ltree import TaggedValue, Segment, LTree
from pyske.slist import SList
from pyske.support.parallel import *
from pyske.support.separate import *
from mpi4py import MPI


TAG_BASE = "270995"
TAG_COMM_REDUCE = int(TAG_BASE + "11")
TAG_COMM_UACC_1 = int(TAG_BASE + "21")
TAG_COMM_UACC_2 = int(TAG_BASE + "22")
TAG_COMM_DACC_1 = int(TAG_BASE + "31")
TAG_COMM_DACC_2 = int(TAG_BASE + "32")
TAG_COMM_MERGE = int(TAG_BASE + "00")


class PTree:
	"""
	A class used to represent a distributed tree

	Attributes
	----------
	__distribution: pid -> nb of segments
	__global_index: num seg -> (start, offset)
	__start_index: index of first index for the current pid in global_index
	__nb_segs: nb of indexes for the current pid in global_index
	__content: concatenation of the segments contained in the current instance
	"""
	def __init__(self, lt = None):
		self.__distribution = SList([])
		self.__global_index = SList([])
		self.__start_index = 0
		self.__nb_segs = 0
		self.__content = SList([])
		if(lt != None):
			(distribution, global_index) = distribute_tree(lt, nprocs)
			self.__distribution = distribution
			self.__global_index = global_index
			self.__start_index = distribution.scan(lambda x, y : x + y, 0)[pid]
			self.__nb_segs = distribution[pid]
			for i_seg in range(self.__start_index, self.__start_index + __nb_segs):
				self.__content.extend(lt[i_seg])


	def init(pt, content):
		"""
		Factory for distributed tree
		"""
		p = PTree()
		p.__distribution = pt.__distribution
		p.__global_index = pt.__global_index
		p.__start_index = pt.__start_index
		p.__nb_segs = pt.__nb_segs
		p.__content = content
		return p


	def init_from_file(filename, parser = int):
		"""
		Instantiate a distributed tree from a file
		"""
		filename = filename + "." + str(pid)
		def __parser_couple(s):
			s = s.replace("(","")
			s = s.replace(")","")
			ss = s.split(",")
			return (int(ss[0]), int(ss[1]))
		p = PTree()
		content = SList([])
		with open(filename,"r") as f:
			count_line = 0
			for line in f:
				if line.strip()[0] == '#':
					continue
				# __distribution: pid -> nb of segments
				# __global_index: num seg -> (start, offset)
				if count_line == 0: # Get the distribution
					p.__distribution = SList.from_str(line)
					p.__start_index = p.__distribution.scan(lambda x, y : x + y, 0)[pid]
					p.__nb_segs = p.__distribution[pid]
				elif count_line == 1: # Get the global_index
					p.__global_index = SList.from_str(line, parser = __parser_couple)
				else: # Get the content
					content.extend(Segment.from_str(line, parser = parser))
				count_line = count_line+1
		p.__content = content
		return p


	def __str__(self):
		return "pid["+str(pid)+"]:\n" + \
			   "  global_index: "+ str(self.__global_index)+ "\n" + \
			   "  distribution: " + str(self.__distribution) + "\n" + \
			   "  nb_segs: " + str(self.__nb_segs) + "\n" + \
			   "  start_index: " + str(self.__start_index) + "\n" + \
			   "  content: "  + str(self.__content) +"\n"


	def browse(self):
		"""
		Browse the linearized distributed tree contained in the current processor
		"""
		res = "pid[" + str(pid) + "] "
		for (start, offset) in self.__global_index[self.__start_index : self.__start_index+self.__nb_segs]:
			seg = Segment(self.__content[start:start+offset])
			res = res + "\n   " + str(seg)
		return res


	def map(self, kl, kn):
		"""
		Map skeleton for distributed tree
		"""
		content = SList([])
		for (start, offset) in self.__global_index[self.__start_index : self.__start_index+self.__nb_segs]:			
			content.extend(Segment(self.__content[start:start+offset]).map_local(kl,kn))
		return PTree.init(self, content)


	def reduce(self, k, phi, psi_n, psi_l, psi_r):
		"""
		Reduce skeleton for distributed tree
		"""
		# Step 1 : Local Reduction
		gt = Segment([])
		for (start, offset) in self.__global_index[self.__start_index : self.__start_index+self.__nb_segs]:
			gt.append(Segment(self.__content[start:start+offset]).reduce_local(k, phi, psi_l, psi_r))
		# Step 2 : Gather local Results
		if pid == 0:
			for i in range(1, nprocs):
				gt.extend(comm.Irecv(source=i, tag=TAG_COMM_REDUCE)['c'])
		else:
			comm.Isend({'c' : gt}, dest=0, tag=TAG_COMM_REDUCE)
		# Step 3 : Global Reduction
		return (gt.reduce_global(psi_n) if pid == 0 else None)
	

	def uacc(self, k, phi, psi_n, psi_l, psi_r):
		"""
		Upward accumulation skeleton for distributed tree
		"""
		# Step 1 : Local Upwards Accumulation
		gt = Segment([])
		lt2 = SList([])
		for (start, offset) in self.__global_index[self.__start_index : self.__start_index+self.__nb_segs]:
			(top, res) = Segment(self.__content[start:start+offset]).uacc_local(k, phi, psi_l, psi_r)
			gt.append(top)
			lt2.append(res)

		# Step 2 : Gather local Results
		if pid == 0:
			for iproc in range(1, nprocs):
				gt.extend(comm.Irecv(source=iproc, tag=TAG_COMM_UACC_1)['c'])
		else:
			comm.Isend({'c' : gt}, dest=0, tag=TAG_COMM_UACC_1)

		# Step 3 : Global Upward Accumulation
		if pid == 0:
			gt2 = gt.uacc_global(psi_n)
			for i in range(len(gt2)):
				if gt2[i].is_node():
					gt2[i] = TaggedValue((gt2.get_left(i).get_value(),gt2.get_left(i).get_value()),gt2[i].get_tag())


		# Step 4 : Distributing Global Result
		start = 0
		if pid == 0:
			for iproc in range(nprocs):
				iproc_off = self.__distribution[iproc]
				if iproc != 0:
					comm.Isend({'g':gt2[start : start + iproc_off]}, dest=iproc,tag = TAG_COMM_UACC_2)
				start = start + iproc_off
		else:
			gt2 = comm.Irecv(source = 0, tag = TAG_COMM_UACC_2)['g']

		# Step 5 : Local Updates
		new_content = SList([])
		for i in range(len(self.__global_index[self.__start_index : self.__start_index+self.__nb_segs])):
			(start, offset) = self.__global_index[self.__start_index : self.__start_index+self.__nb_segs][i]
			if gt[i].is_node():
				(lc,rc) = gt2[i].get_value()
				val = Segment(self.__content[start:start+offset]).uacc_update(lt2[i], k, lc, rc)
			else:
				val = lt2[i]
			new_content.extend(val)

		return PTree.init(self, new_content)
			

	def dacc(self, gl, gr, c, phi_l, phi_r, psi_u, psi_d):
		"""
		Downward accumulation skeleton for distributed tree
		"""
		# Step 1 : Computing Local Intermediate Values
		gt = Segment([])
		for (start, offset) in self.__global_index[self.__start_index : self.__start_index+self.__nb_segs]:			
			seg = Segment(self.__content[start:start+offset])
			if seg.has_critical():
				gt.append(seg.dacc_path(phi_l, phi_r, psi_u))
			else:
				gt.append(TaggedValue(seg[0].get_value(), "L"))
		# Step 2 : Gather Local Results
		if pid == 0:
			for iproc in range(1, nprocs):
				gt.extend(comm.Irecv(source=iproc, tag=TAG_COMM_DACC_1)['c'])
		else:
			comm.Isend({'c' : gt}, dest=0, tag=TAG_COMM_DACC_1)
		# Step 3 : Global Downward Accumulation
		gt2 = (gt.dacc_global(psi_d, c) if pid == 0 else None)
		# Step 4 : Distributing Global Result
		if pid == 0:
			start = 0
			for iproc in range(nprocs):
				iproc_off = self.__distribution[iproc]
				if iproc != 0:
					comm.Isend({'g':gt2[start : start + iproc_off]}, dest=iproc,tag = TAG_COMM_UACC_2)
				start = start + iproc_off
		else:
			gt2 = comm.Irecv(source = 0, tag = TAG_COMM_UACC_2)['g']
		# Step 5 : Local Downward Accumulation
		new_content = SList([])
		for i in range(len(self.__global_index[self.__start_index : self.__start_index+self.__nb_segs])):
			(start, offset) = self.__global_index[self.__start_index : self.__start_index+self.__nb_segs][i]
			# new_content.extend(Segment(self.__content[start:start+offset]).dacc_local(gl, gr, gt2[self.__start_index + i].get_value()))
			new_content.extend(Segment(self.__content[start:start+offset]).dacc_local(gl, gr, gt2[i].get_value()))
		return PTree.init(self, new_content)


	def zip(self, pt):
		"""
		Zip skeleton for distributed tree
		"""
		assert self.__distribution == pt.__distribution
		new_content = SList([])
		for i in range(len(self.__global_index[self.__start_index : self.__start_index+self.__nb_segs])):
			(start, offset) = self.__global_index[self.__start_index : self.__start_index+self.__nb_segs][i]
			new_content.extend(Segment(self.__content[start:start+offset]).zip(Segment(pt.__content[start:start+offset])))
		return PTree.init(self, new_content)


	def zipwith(self, pt, f):
		"""
		Zipwith skeleton for distributed tree
		"""
		assert self.__distribution == pt.__distribution
		new_content = SList([])
		for i in range(len(self.__global_index[self.__start_index : self.__start_index+self.__nb_segs])):
			(start, offset) = self.__global_index[self.__start_index : self.__start_index+self.__nb_segs][i]
			new_content.extend(Segment(self.__content[start:start+offset]).zipwith(Segment(pt.__content[start:start+offset]),f))
		return PTree.init(self, new_content)
