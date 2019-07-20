import pyske.core.opt.fun as fun
import pyske.core.opt.util as util
from pyske.core.list.plist import PList as PL
from pyske.core.opt.list import PList
from pyske.core.support.parallel import at_root, barrier, wtime, nprocs
from operator import add, mul
import random
import argparse
import gc

# Command-line arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("--size", help="size of the list to generate", type=int, default=1_000_000)
parser.add_argument("--iter", help="number of iterations", type=int, default=30)
parser.add_argument("--test", help="choice of the test",
                    choices=['direct', 'wrapper', 'optimized', 'hand_optimized'],
                    default='direct')
args = parser.parse_args()
size = args.size
test = args.test

random.seed(42)

# Creation of input lists
def rand(i):
    return random.randint(0, 100)


pl1 = PL.init(rand, size)

pl2 = PL.init(rand, size)

# ------ Example: dot product --------

# wrapped or direct uncurry
uncurry = util.uncurry if test in ['direct', 'hand_optimized'] else fun.uncurry

# If using the automatic optimization, the parallel lists of type PL
# should be wrapped.
def wrap(pl):
    if test in ['direct', 'hand_optimized']:
        return pl
    else:
        return PList.raw(pl)


def dot_product():
    return wrap(pl2).zip(wrap(pl1)).map(uncurry(mul)).reduce(add, 0)


def compute():
    if test == 'direct':
        return dot_product()
    elif test == 'wrapper':
        return dot_product().eval()
    elif test == 'optimized':
        return dot_product().run()
    elif test == 'hand_optimized':
        return pl2.map2(mul, pl1).reduce(add, 0)


def main():
    at_root(lambda: print("Test:\t", test))
    for i in range(0, args.iter):
        gc.collect()
        barrier()
        t = PL.init(lambda _: wtime(), nprocs)
        result = compute()
        elapsed = t.map(lambda x: wtime() - x)
        max_elapsed = elapsed.reduce(max)
        avg_elapsed = elapsed.reduce(add) / nprocs
        all_elapsed = elapsed.mapi(lambda i, x: "[" + str(i) + "]:" + str(x)).to_seq()
        at_root(lambda:
                print(f'Iteration:\t{i}\n'
                      f'Result:\t{result}\n'
                      f'Time (max):\t{max_elapsed}\n'
                      f'Time (avg):\t{avg_elapsed}\n'
                      f'Time (all):\t{all_elapsed}'))


main()

