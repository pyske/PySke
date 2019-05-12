import sys
import random
import argparse

from pyske.core.list.plist import PList
from pyske.core.support.parallel import *

parser = argparse.ArgumentParser()
parser.add_argument("-n", help="size ot he list to generate", type=int)

# --------------------- #

# Generating a parallel list of the size specified on the command line or 1000
if len(sys.argv) > 1:
    args = parser.parse_args()
    size = args.n
else:
    size = 1000
X = PList.init(lambda _: bool(random.getrandbits(1)), size)

comm.barrier()

# computing the variance
# Solution 1
X.map(lambda x: not x).reduce(lambda x, y: x and y)
# Solution 2
X.map_reduce(lambda x: not x, lambda x, y: x and y)
# Solution 3
not (X.reduce(lambda x, y: x or y))
