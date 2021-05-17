from pyske.core.interface import List


def int_to_tuple(num):
    return num, num


def max_subarray(_sum, num):
    best_sum, current_sum = _sum
    x, y = num
    current_sum = max(0, current_sum + x)
    best_sum = max(best_sum, current_sum)
    return best_sum, current_sum


def max_subarray_problem_(input_list: List):
    """
    return the maximum sum of a contiguous subarray of the list

    Examples::

        >>> from pyske.core import PList, SList
        >>> max_subarray_problem_(SList([-5 , 2 , 6 , -4 , 5 , -6 , -4 , 3]))
        9
        >>> max_subarray_problem_(PList.from_seq([-33 , 22 , 11 , -44]))
        33

    :param input_list: a PySke list of numbers
    :return: a number, the maximum sum of a subarray
    """
    best_sum, _ = input_list.map(int_to_tuple).reduce(max_subarray, (0, 0))
    return best_sum
