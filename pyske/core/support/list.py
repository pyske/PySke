"""
Supporting functions on Python lists.
"""

from typing import TypeVar, Callable, List


T = TypeVar('T')  # pylint: disable=invalid-name
R = TypeVar('R')  # pylint: disable=invalid-name


def scan(a_list: List[T],
         binary_op: Callable[[R, T], R],
         neutral: R) -> 'List[R]':
    """
    Return the full prefix-sum list.

    The returned list has more additional element than ``a_list``.
    The first element of the new list is ``neutral``.

    Example::

        >>> scan([1, 2, 3], lambda x, y: x + y, 0)
        [0, 1, 3, 6]

    :param a_list: a list, possibly containing elements of a different type than ``neutral``.
    :param binary_op: binary associative operator
    :param neutral: a value that should be a neutral element for the operation,
        i.e. for all element e,
            ``binary_op(neutral, e) == binary_op(e, neutral) == e``.
    :return: a new list.
    """
    res = a_list.copy()
    res.append(neutral)
    res[0] = neutral
    for i in range(1, len(res)):
        neutral = binary_op(neutral, a_list[i - 1])
        res[i] = neutral
    return res
