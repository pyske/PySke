"""
Execution of k_means
"""
import gc

from pyske.core import Timing
from pyske.examples.list.k_means import k_means
from pyske.examples.list import util
import matplotlib.pyplot as plt
import argparse

PAR = 'parallel'
SEQ = 'sequential'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--size", help="size of the list to generate", type=int, default=1_000_000)
    parser.add_argument("--iter", help="number of iterations", type=int, default=30)
    parser.add_argument("--data", help="type of data structure", choices=[PAR, SEQ], default=SEQ)
    parser.add_argument("--clusters", help="number of clusters", type=int, default=3)

    args = parser.parse_args()
    size = args.size
    num_iter = args.iter
    choice = args.data
    clusters = args.clusters

    pyske_list_class = util.select_pyske_list(choice)
    input_list = util.rand_point_list(pyske_list_class, size, clusters)
    timing = Timing()
    execute = util.select_execute(choice)
    example = k_means
    execute(lambda: print('Version:\t', choice))
    gc.disable()
    for iteration in range(1, 1 + num_iter):
        timing.start()
        result = example(input_list, clusters)
        timing.stop()
        gc.collect()
        util.print_experiment("", timing.get(), execute, iteration)
        for i in range(len(result)):
            plt.scatter([point.x for point in result[i]], [point.y for point in result[i]])
        plt.show()
