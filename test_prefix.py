from pyske.ptree import PTree
from pyske.applications.parallel.prefix import prefix
from pyske.support.parallel import *

import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="name of the files that contain the PTree parts")
parser.add_argument("-nt", help="number of tests to do", type = int)
args = parser.parse_args()

filename = args.f
if filename[-3:] != ".pt":
	filename = filename + ".pt"

pt = PTree.init_from_file(filename)
ntest = args.nt

# for i in range(0,nprocs):
#     MPI.COMM_WORLD.Barrier()
#     if pid == i:
#         print ('Rank %d out of %d' % (pid,nprocs))


for i in range(ntest):
	try:
		comm.barrier()
		start_time = time.time()
		res = prefix(pt)
		comm.barrier()
		end_time = time.time()
		at_root(lambda : print(str(nprocs) + "\t" + str(format(end_time-start_time, '.6f')) + "\t" + "OK" ))
	except: 
		comm.barrier()
		end_time = time.time()
		at_root(lambda : print(str(nprocs) + "\t" + str(format(end_time-start_time, '.6f')) + "\t" + "KO" ))


