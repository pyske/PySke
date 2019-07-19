import random
import argparse

from pyske.core.list.plist import PList
from pyske.core.support.parallel import *

parser = argparse.ArgumentParser()
parser.add_argument("-n", help="size of the list to generate", type=int, default=1000)
parser.add_argument("-a", help="choice of the algorithm (1-3)", type=int, default=1)
parser.add_argument("-s", help="choice of a seed", type=int, default=111)

# --------------------- #

# Generating a parallel list of the size specified on the command line or 1000
args = parser.parse_args()
size = args.n
algorithm = args.a
seed = args.s

random.seed(seed)

X = PList.init(lambda _: bool(random.getrandbits(1)), size)

comm.barrier()

# computing the variance
# Solution 1
if algorithm == 1:
    res = X.map(lambda x: not x).reduce(lambda x, y: x and y)
# Solution 2
if algorithm == 2:
    res = X.map_reduce(lambda x: not x, lambda x, y: x and y, True)
if algorithm == 3:
# Solution 3
    res = not (X.reduce(lambda x, y: x or y, False))

at_root(lambda : print(res))


