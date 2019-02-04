from mpi4py import MPI

comm = MPI.COMM_WORLD
pid = comm.Get_rank()
nprocs = comm.Get_size()

def local_size_pid(pid, size):
	return int(size / nprocs) + (1 if pid < size % nprocs else 0)

def local_size(size):
	return local_size_pid(pid, size)

def at_root(f):
	if pid == 0:
		return f()
	else:
		return None