"""
Computation of the conjonction of the negation of a list of Boolean values
"""

import random
import argparse

from pyske.core.list import PList
from pyske.core.util import par

__all__ = []


def __main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="size of the list to generate", type=int, default=1000)
    parser.add_argument("-a", help="choice of the algorithm (1-3)", type=int, default=1)
    parser.add_argument("-s", help="choice of a seed", type=int, default=111)
    # Generating a parallel list of the size specified on the command line or 1000
    args = parser.parse_args()
    size = args.n
    algorithm = args.a
    seed = args.s
    random.seed(seed)
    data = PList.init(lambda _: bool(random.getrandbits(1)), size)
    par.barrier()
    # Solution 1
    if algorithm == 1:
        res = data.map(lambda x: not x).reduce(lambda x, y: x and y)
    # Solution 2
    if algorithm == 2:
        res = data.map_reduce(lambda x: not x, lambda x, y: x and y, True)
    # Solution 3
    if algorithm == 3:
        res = not data.reduce(lambda x, y: x or y, False)
    if algorithm in [1, 2, 3]:
        par.at_root(lambda: print(res))


if __name__ == '__main__':
    __main()
