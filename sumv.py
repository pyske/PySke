from pyske.core.tree.ptree import PTree
from pyske.core.support.parallel import *

from pyske.application.tree.sumv import sumv

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

for i in range(ntest):
	try:
		comm.barrier()
		start_time = time.time()
		res = sumv(pt)
		comm.barrier()
		end_time = time.time()
		at_root(lambda : print(str(nprocs) + "\t" + str(format(end_time-start_time, '.6f')) + "\t" + str(res) ))
	except Exception as e: 
		comm.barrier()
		end_time = time.time()
		at_root(lambda : print(e))
		# at_root(lambda : print(str(nprocs) + "\t" + str(format(end_time-start_time, '.6f')) + "\t" + "KO" ))


