"""
Execution of k_means
"""
import argparse

from pyske.core import Timing
from pyske.examples.list.k_means import k_means, k_means_init
from pyske.examples.list import util

PAR = 'parallel'
SEQ = 'sequential'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--size", help="size of the list to generate", type=int, default=1_000)
    parser.add_argument("--iter", help="number of iterations", type=int, default=30)
    parser.add_argument("--data", help="type of data structure", choices=[PAR, SEQ], default=SEQ)
    parser.add_argument("--clusters", help="number of clusters", type=int, default=3)
    parser.add_argument("--dimensions", help="point dimensions", type=int, default=2)
    parser.add_argument("--show-clusters", help="display the clusters graph of 2D points",
                        action="store_true")

    args = parser.parse_args()
    size = args.size
    num_iter = args.iter
    choice = args.data
    clusters = args.clusters
    dimensions = args.dimensions
    show_clusters = args.show_clusters

    pyske_list_class = util.select_pyske_list(choice)
    input_list = util.rand_point_list(pyske_list_class, size, clusters, dimensions)

    timing = Timing()
    execute = util.select_execute(choice)
    example = k_means
    execute(lambda: print('Version:\t', choice))
    for iteration in range(1, 1 + num_iter):
        timing.start()
        result = example(input_list, k_means_init, clusters)
        timing.stop()
        util.print_experiment("", timing.get(), execute, iteration)
        if show_clusters and dimensions == 2:
            util.print_2D_result(result.to_seq())
