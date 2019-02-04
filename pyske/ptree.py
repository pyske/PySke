from pyske.ltree import TaggedValue, Segment, LTree
from pyske.slist import SList
from pyske.support.parallel import *

TAG_BASE = "270995"
TAG_COMM_REDUCE = int(TAG_BASE + "1")

TAG_COMM_UACC = 120102
TAG_COMM_DACC = 126722


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
			size = lt.length()

			start_global_index = 0
			for proc_id in range(nprocs):
				start_index = 0

				nsegs = local_size_pid(proc_id, size)
				self.__distribution.append((proc_id, nsegs))
				for seg_idx in range(start_global_index, start_global_index + nsegs):
					self.__global_index.append((start_index, lt[seg_idx].length()))
					start_index = start_index + lt[seg_idx].length() 

					if proc_id == pid:
						self.__content.extend(lt[seg_idx])
				if proc_id == pid:
					self.__start_index = start_global_index
					self.__nb_segs = nsegs

				start_global_index = start_global_index + nsegs


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
		# Step 1 : Reduce local
		gt = Segment([])
		for (start, offset) in self.__global_index[self.__start_index : self.__start_index+self.__nb_segs]:
			gt.append(Segment(self.__content[start:start+offset]).reduce_local(k, phi, psi_l, psi_r))
		# Step 2 : Gather Results
		if pid == 0:
			for i in range(1, nprocs):
				gt.extend(comm.recv(source=i, tag=TAG_COMM_REDUCE)['c'])
		else:
			comm.send({'c' : gt}, dest=0, tag=TAG_COMM_REDUCE)
		# Step 3 : Reduce global
		return (gt.reduce_global(psi_n) if pid == 0 else None)
	

	# TODO : below must be debugged !

	def uacc(self, k, phi, psi_n, psi_l, psi_r):
		"""
		TODO
		"""

		# TODO fix the communication of step 2 and step 3 cause we need to use
		# the global gt2. Instead of using (_,_) in idx (step 3), we need to
		# to use the global idx ! And only use the one we need. Create a res
		# segment for there representing the resulting segment of a small part only

		# STEP 1 : uacc locally applied #
		seg2 = Segment()
		gt_l = Segment()
		for (start, offset) in idx:
			seg = Segment(self.content[start:start+offset])
			(res_local, gt_local) = seg.uacc_local(k, phi, psi_l, psi_r)
			seg2 = seg2 + res_local
			gt_l = gt_l + gt_local

		comm.gather(gt_l, root=0)

		# STEP 2 : uacc global executed at root #
		if pid == 0:
			gt = Segment()
			for i in range(size):
				gt = gt + gt_l[i]
			gt2 = gt.uacc_global(psi_n)

			passed = len(idx)
			for i in range(1, size):
				data = {'gt2': gt2[passed + 1 : passed + 1 + proc_nb[i]]}
				comm.send(data, dest=i, tag=TAG_COMM_UACC)
				passed = passed + 1 + proc_nb[i]
			gt2 = gt2[0: len(idx)]

		else:
			data = comm.recv(source = 0, tag=TAG_COMM_UACC)
			gt2 = data['gt2']

		# STEP 3 #
		res_l = Segment()
		for i in range(gt2.length()):
			(start, offset) = idx[i]
			seg_2_up = Segment(seg2[start:start+offset])
			if gt2[i].is_node():
				seg_up = Segment(self.content[start:start+offset])
				res_l = res_l + seg_up.uacc_update(k, seg_2_up, gt2[i].get_value())
			else:
				res_l = res_l + seg_2_up

		return PTree(res_l, idx)

			
	def dacc(self, gl, gr, c, phi_l, phi_r, psi_u, psi_d):
		"""
		TODO
		"""
		# STEP 1 : dacc_path #
		gt_l = Segment()
		for (start, offset) in idx:
			seg = Segment(self.content[start:start+offset])
			gt_l.append(seg.dacc_path(phi_l, phi_r, psi_u, psi_d))
		
		comm.gather(gt_l, root=0)

		# STEP 2 :  at root #

		if pid == 0:
			gt = Segment()
			for i in range(size):
				gt = gt + gt_l[i]
			gt2 = gt.dacc_global(psi_d, c)

			passed = len(idx)
			for i in range(1, size):
				data = {'gt2': gt2[passed + 1 : passed + 1 + proc_nb[i]]}
				comm.send(data, dest=i, tag=TAG_COMM_DACC)
				passed = passed + 1 + proc_nb[i]
			gt2 = gt2[0: len(idx)]

		else:
			data = comm.recv(source = 0, tag=TAG_COMM_DACC)
			gt2 = data['gt2']


		# STEP 3 : 	#
		seg2 = Segment()
		for i in range(gt2.length()):
			seg = Segment(self.content[start:start+offset])
			seg2.append(seg.append(gl, gr, gt2[i]))

		return PTree(seg2, idx)

