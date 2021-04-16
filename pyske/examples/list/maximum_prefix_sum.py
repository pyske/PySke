"""
Maximum Prefix Sum
"""

from pyske.core.interface import List


# ------- Maximum Prefix Sum ------------

def _max0_copy(num):
    return max(0, num), num


def _max_sum(pair_a, pair_b):
    a_m, a_s = pair_a
    b_m, b_s = pair_b
    max_ = max(a_m, a_s + b_m)
    sum_ = a_s + b_s
    return max_, sum_


def mps(input_list: List):
    """
    Return the maximum prefix sum.

    Examples::

        >>> from pyske.core import PList, SList
        >>> mps(SList([1, 2, -1, 2, -1, -1, 3, -4]))
        5
        >>> mps(PList.from_seq([-12, -2, -42]))
        0

    :param input_list: a PySke list of numbers
    :return: a number, the maximum prefix sum
    """
    max_, _ = input_list.map(_max0_copy).reduce(_max_sum, (0, 0))
    return max_
