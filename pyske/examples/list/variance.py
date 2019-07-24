from pyske.core.list.plist import PList
from pyske.core.util import par
import sys
import random
from operator import add

# Generating a parallel list of the size specified on the command line or 1000
if len(sys.argv) > 1:
    size = int(sys.argv[1])
else:
    size = 1000
X = PList.init(lambda _: 50+random.randint(0, 10), size)

par.barrier()

# start timing
t = PList.init(lambda _: par.wtime())

# computing the variance
n = X.length()
avg = X.reduce(add) / n


def f(x): return (x-avg) ** 2


var = X.map(f).reduce(add) / n

# stop timing
elapsed = t.map(lambda x: par.wtime() - x)
max_elapsed = elapsed.reduce(max)
avg_elapsed = elapsed.reduce(add) / elapsed.length()
all_elapsed = elapsed.mapi(lambda i, x: "[" + str(i) + "]:" + str(x)).to_seq()

# output at processor 0
par.at_root(lambda:
            print(f'Variance:\t{var}\nTime (max):\t{max_elapsed}\n'
                  f'Time (avg):\t{avg_elapsed}\nTime (all):\t{all_elapsed}'))
