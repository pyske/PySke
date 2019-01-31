from pyske.ltree import LTree
from pyske.ptree import PTree
from pyske.slist import SList
from mpi4py import MPI

comm = MPI.COMM_WORLD
pid = comm.Get_rank()
nprocs = comm.Get_size()

def local_size(pid, size):
	return int(size / pid) + (1 if pid < size % pid else 0)

def local_size(size):
	return local_size(pid, size)

def distribute_tree(lt):
	idx = SList()
	content = SList()

	size = lt.length()
	rem = size % nprocs
	lsz = int(size / nprocs)

	drops = pid * lsz + pid if pid < rem else rem
	takes = lsz + 1 if pid < rem else 0
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
	if pid == 0:
		return f()
	else:
		return None