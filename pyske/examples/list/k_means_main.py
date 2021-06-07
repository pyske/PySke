"""
Execution of k_means
"""

from pyske.core import Timing
from pyske.examples.list.k_means import k_means, k_means_init
from pyske.examples.list import util

PAR = 'parallel'
SEQ = 'sequential'


if __name__ == '__main__':

    parser = util. k_means_parser()

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
