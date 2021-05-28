"""
The Maximum Segment Sum (MSS) problem
"""
from pyske.core.interface import List


def int_to_tuple(num):
    """Duplicate a value into a pair of values"""
    return num, num


def max_and_sum(_sum, number_pair):
    """From the best sum, current sum, and a new value, generate the new best and current sum"""
    best_sum, current_sum = _sum
    number, _ = number_pair
    current_sum = max(0, current_sum + number)
    best_sum = max(best_sum, current_sum)
    return best_sum, current_sum


def maximum_segment_sum(input_list: List):
    """
    Return the maximum sum of the segments of a list

    Examples::

        >>> from pyske.core import PList, SList
        >>> maximum_segment_sum(SList([-5 , 2 , 6 , -4 , 5 , -6 , -4 , 3]))
        9
        >>> maximum_segment_sum(PList.from_seq([-33 , 22 , 11 , -44]))
        33
        >>> maximum_segment_sum(PList.from_seq([-33 , 22 , 0, 1, -3, 11 , -44, 30, -5, -13, 12]))
        31

    :param input_list: a PySke list of numbers
    :return: a number, the maximum sum of the segments of a list
    """
    best_sum, _ = input_list.map(int_to_tuple).reduce(max_and_sum, (0, 0))
    return best_sum
