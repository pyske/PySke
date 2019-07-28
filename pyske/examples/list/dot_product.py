"""
Dot product of two vectors implemented as parallel lists
"""

import random
import argparse
import gc
from operator import add, mul
from pyske.core.util import fun
from pyske.core.opt import fun as opt
from pyske.core.list.plist import PList as DPList
from pyske.core.opt.list import PList
from pyske.core.util.par import at_root, barrier
from pyske.core import timing

__all__ = []


def __rand(_):
    return random.randint(0, 100)


def __wrap(test):
    if test in ['direct', 'hand_optimized']:
        return fun.idt
    return PList.raw


def __dot_product(wrapper, uncurry, pl1: DPList, pl2: DPList):
    new_pl1 = wrapper(pl1)
    new_pl2 = wrapper(pl2)
    return new_pl2.zip(new_pl1).map(uncurry(mul)).reduce(add, 0)


def __print_info(iteration, result, max_value, avg_value, all_values):
    return lambda: \
        print(f'Iteration:\t{iteration}\n'
              f'Result:\t{result}\n'
              f'Time (max):\t{max_value}\n'
              f'Time (avg):\t{avg_value}\n'
              f'Time (all):\t{all_values}')


def __compute(test, pl1, pl2):
    uncurry = fun.uncurry if test in ['direct', 'hand_optimized'] else opt.uncurry
    wrapper = __wrap(test)
    if test == 'direct':
        return __dot_product(wrapper, uncurry, pl1, pl2)
    if test == 'wrapper':
        return __dot_product(wrapper, uncurry, pl1, pl2).eval()
    if test == 'optimized':
        return __dot_product(wrapper, uncurry, pl1, pl2).run()
    if test == 'hand_optimized':
        return pl2.map2(mul, pl1).reduce(add, 0)
    return DPList()


def __main():
    time = timing.Timing()
    random.seed(42)
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
    # Creation of input lists
    pl1 = DPList.init(__rand, size)
    pl2 = DPList.init(__rand, size)
    at_root(lambda: print("Test:\t", test))
    for iteration in range(0, args.iter):
        gc.collect()
        barrier()
        time.start()
        result = __compute(test, pl1, pl2)
        time.stop()
        max_elapsed, avg_elapsed, all_elapsed = time.get()
        at_root(__print_info(iteration, result, max_elapsed, avg_elapsed, all_elapsed))


__main()
