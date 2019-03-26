from pyske.core.list.slist import SList
from pyske.core.list.plist import PList
from pyske.core.support.parallel import *
import sys, random
from operator import add
from mpi4py import MPI

# Generating a parallel list of the size specified on the command line or 1000
if len(sys.argv) > 1:
    size = int(sys.argv[1])
else:
    size = 1000
X = PList.init(lambda _: 50+random.randint(0, 10), size)

comm.barrier()

# start timing
t = PList.init(lambda _: wtime(), nprocs)

# computing the variance
n = X.length()
avg = X.reduce(add) / n
def f(x): return (x-avg) ** 2
var = X.map(f).reduce(add) / n

# stop timing
elapsed = t.map(lambda x: wtime() - x)
max_elapsed = elapsed.reduce(max)
avg_elapsed = elapsed.reduce(add) / nprocs
all_elapsed = elapsed.mapi(lambda i, x: "[" + str(i) + "]:" + str(x)).to_seq()

# output at processor 0
at_root(lambda:
        print(f'Variance:\t{var}\nTime (max):\t{max_elapsed}\n'
              f'Time (avg):\t{avg_elapsed}\nTime (all):\t{all_elapsed}'))
