from pyske.ltree import TaggedValue, Segment, LTree
from mpi4py import MPI

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
size = comm.Get_size()

global proc_nb #= comm.get("proc_nb") #Global, TODO : how to do it ?
global total_size #= comm.get("total_size") #Global, TODO : how to do it ? really useful?

TAG_COMM_UACC = 120102
TAG_COMM_DACC = 126722

 

class PTree:
	"""
	TODO
	"""

	def __init__(self, content, idx):
		self.content = content
		self.total_size = total_size
		self.idx = idx


	def get_content(self):
		return self.content


	def get_total_size(self):
		return self.total_size


	def map(self, kl, kn):
		"""
		TODO
		"""
		res_l = SList()
		for (start, offset) in idx:
			seg = Segment(self.content[start:start+offset])
			res_l = res_l + seg.map_local(kl,kn)
		return PTree(res_l, idx)


	def reduce(self, k, phi, psi_n, psi_l, psi_r):
		"""
		TODO
		"""
		res_l = Segment()
		for (start, offset) in idx:
			seg = Segment(self.content[start:start+offset])
			res_l = res_l + seg.reduce_local(k, phi, psi_l, psi_r)
		comm.gather(res_l, root=0)
		if my_rank == 0:
			gt = Segment()
			for i in range(size):
				gt.append(res_l[i])
			return gt.reduce_global(psi_n)
		else:
			return None


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
		if my_rank == 0:
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

		if my_rank == 0:
			gt = Segment()
			for i in range(size):
				gt = gt + gt_l[i]
			gt2 = gt.dacc_global(psi_d, c)

			passed = len(idx)
			for i in range(1, size):
				data = {'gt2': gt2[passed + 1 : passed + 1 + proc_nb[i]]}
				comm.send(data, dest=i, tag=TAG_COMM_UACC)
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

