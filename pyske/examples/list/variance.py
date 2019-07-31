"""
Variance Example
"""
import sys
import random
from operator import add
from pyske.core import PList, Timing, par


def variance(data):
    """Return the variance of a random variable"""
    size = data.length()
    avg = data.reduce(add) / size
    var = data.map(lambda num: (num - avg) ** 2).reduce(add) / size
    return var


def _main():
    time = Timing()
    # Generating a parallel list of the size specified on the command line or 1000
    size = 1000
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    data = PList.init(lambda _: 50+random.randint(0, 10), size)
    par.barrier()
    # start timing
    time.start()
    # computing the variance
    var = variance(data)
    # stop timing
    time.stop()
    # output at processor 0
    max_elapsed, avg_elapsed, all_elapsed = time.get()
    par.at_root(lambda:
                print(f'Variance:\t{var}\nTime (max):\t{max_elapsed}\n'
                      f'Time (avg):\t{avg_elapsed}\nTime (all):\t{all_elapsed}'))


if __name__ == '__main__':
    _main()
