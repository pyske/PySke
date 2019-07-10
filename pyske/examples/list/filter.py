from pyske.core.list.plist import PList
from pyske.core.support.parallel import *
import sys
import random
from operator import add

# Generating a parallel list of the size specified on the command line or 1000
if len(sys.argv) > 1:
    size = int(sys.argv[1])
else:
    size = 1000
X = PList.init(lambda _: 50+random.randint(0, 100), size)

comm.barrier()

# start timing
t = PList.init(lambda _: wtime(), nprocs)

# filter out odd values and get the distribution after balancing
def p(x): return x % 2 == 0
d = X.get_partition().map(lambda l: l.filter(p)).flatten().balance().get_partition().map(len).to_seq()

# stop timing
elapsed = t.map(lambda x: wtime() - x)

max_elapsed = elapsed.reduce(max)
avg_elapsed = elapsed.reduce(add) / nprocs
all_elapsed = elapsed.mapi(lambda i, x: "[" + str(i) + "]:" + str(x)).to_seq()

# output at processor 0
at_root(lambda:
        print(f'Distribution: \t{d}\nTime (max): \t{max_elapsed}\n'
              f'Time (avg): \t{avg_elapsed}\nTime (all): \t{all_elapsed}'))
