"""
Execution of k_means
"""
import gc

from pyske.core import Timing
from pyske.examples.list.k_means import k_means
from pyske.examples.list import util


if __name__ == '__main__':
    size, num_iter, choice = util.standard_parse_command_line()
    pyske_list_class = util.select_pyske_list(choice)
    input_list = util.rand_point_list(pyske_list_class, size)
    timing = Timing()
    execute = util.select_execute(choice)
    example = k_means
    execute(lambda: print('Version:\t', choice))
    gc.disable()
    for iteration in range(1, 1 + num_iter):
        timing.start()
        result = example(input_list, 5)
        timing.stop()
        gc.collect()
        util.print_experiment(result, timing.get(), execute, iteration)