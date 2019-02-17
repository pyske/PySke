from mpi4py import MPI

comm = MPI.COMM_WORLD
pid = comm.Get_rank()
nprocs = comm.Get_size() 

def time():
	return MPI.Wtime()

def local_size_pid(pid, size):
	return int(size / nprocs) + (1 if pid < size % nprocs else 0)

def local_size(size):
	return local_size_pid(pid, size)

def at_root(f):
	if pid == 0:
		return f()
	else:
		return None

def scan(op, x,):
	xs = comm.alltoall([x for _ in range(0,nprocs)])
	res = xs[0]
	for i in range(1,pid):
		res=op(res,xs[i])
	return res

def get_conc_reader(filename):
	return MPI.File.Open(comm, filename, MPI.MODE_RDONLY)


def close_conc_file(file):
	return MPI.Close(file)

def run_ptests(tests, filename = ""):
	for f in tests:
		try :
			f()
			at_root(lambda: print("\033[32m[OK] " +str(f)[10:][:-16] + " (test/"+str(filename) +".py)\033[0m"))
		except Exception as e:
			at_root(lambda: print("\033[31m[KO] " +str(f) + " (test/"+str(filename) +".py)\033[0m"))
			at_root(lambda: print(e))