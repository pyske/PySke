"""
Maximum Prefix Sum
"""

from pyske.core.interface import List as IList


# ------- Maximum Prefix Sum ------------


def _max0_copy(num):
    return max(0, num), num


def _max_sum(pair_a, pair_b):
    a_m, a_s = pair_a
    b_m, b_s = pair_b
    max_ = max(0, a_m, a_s + b_m)
    sum_ = a_s + b_s
    return max_, sum_


def mps(data: IList):
    """
    Return the maximum prefix sum.

    Examples::

        >>> from pyske.core import PList, SList
        >>> mps(SList([1, 2, -1, 2, -1, -1, 3, -4]))
        5
        >>> mps(SList([1, 2, -1, 2, -1, 0, 3, -4]))
        6

    :param data: a PySke list of numbers
    :return: a number, the maximum prefix sum
    """
    max_, _ = data.map(_max0_copy).reduce(_max_sum, (0, 0))
    return max_


# -------------- Execution --------------


_PAR = 'parallel'
_SEQ = 'sequential'


def _parse_command_line():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", help="size of the list to generate", type=int, default=1_000_000)
    parser.add_argument("--iter", help="number of iterations", type=int, default=30)
    parser.add_argument("--data", help="type of data structure", choices=[_PAR, _SEQ], default=_SEQ)
    args = parser.parse_args()
    return max(0, args.size), max(0, args.iter), args.data


def _select_pyske_list(choice):
    if choice == _PAR:
        from pyske.core import PList as List
    else:
        from pyske.core import SList as List
    return List


def _select_execute(choice):
    if choice == _PAR:
        from pyske.core.util import par
        return par.at_root
    return lambda f: f()


def _generate_data(cls, size):
    import random
    return cls.init(lambda _: float(random.randint(-100, 100)), size)


def _print(iteration, result, timing, execute):
    avg_t, max_t, all_t = timing
    execute(lambda: print(f'Iteration:\t{iteration}\n'
                          f'Result:\t{result}\n'
                          f'Timing (average):\t{avg_t}\n'
                          f'Timing (maximum):\t{max_t}\n'
                          f'Timing (all): \t{all_t}\n'))


def _main():
    from pyske.core import Timing
    size, num_iter, choice = _parse_command_line()
    pyske_list = _select_pyske_list(choice)
    data = _generate_data(pyske_list, size)
    timing = Timing()
    execute = _select_execute(choice)
    for iteration in range(1, 1 + num_iter):
        timing.start()
        result = mps(data)
        timing.stop()
        _print(iteration, result, timing.get(), execute)


if __name__ == '__main__':
    _main()
