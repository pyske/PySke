"""
Execution of regular_samping_sort.py
"""
import gc
from pyske.core import Timing
from pyske.examples.list import util
from pyske.examples.list.regular_sampling_sort import pssr, is_sorted


def _main():
    size, num_iter, choice = util.standard_parse_command_line()
    pyske_list_class = util.select_pyske_list(choice)
    input_list = util.rand_list(pyske_list_class, size)
    timing = Timing()
    execute = util.select_execute(choice)
    example = pssr if choice == util.PAR else sorted
    execute(lambda: print('Version:\t', choice))
    gc.disable()
    for iteration in range(1, 1 + num_iter):
        timing.start()
        result = example(input_list)
        timing.stop()
        gc.collect()
        if choice == util.PAR:
            assert is_sorted(result)
        result = len(result)
        util.print_experiment(result, timing.get(), execute, iteration)


if __name__ == '__main__':
    _main()
