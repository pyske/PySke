from pyske.ltree import LTree
from pyske.ptree import PTree
from pyske.slist import SList
from mpi4py import MPI

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
nb_procs = comm.Get_size()

def distribute_tree(lt):
	idx = SList()
	content = SList()

	size = lt.length()
	rem = size % nb_procs
	lsz = int(size / nb_procs)

	drops = my_rank * lsz + my_rank if my_rank < rem else rem
	takes = lsz + 1 if my_rank < rem else 0 
	segs = lt[drops : drops + takes]

	start = 0
	for seg in segs :
		for v in seg:
			content.append(v)
		offset = seg.length()
		idx.append((start,offset))
		start = start + offset

	return PTree(content, idx)



def at_root(f):
	if my_rank == 0:
		return f()
	else:
		return None