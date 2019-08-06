"""
A module of useful simple functions.
"""
__all__ = ['idt', 'compose', 'curry', 'uncurry', 'zero', 'one', 'add', 'incr', 'decr',
           'is_even', 'is_odd']

import functools
import operator


def idt(value):
    """
    The identity function.

    :param value: anything
    :return: its input
    """
    return value


def compose(fun_f, fun_g):
    """
    Composition of two functions.

    :param fun_f: callable
    :param fun_g: callable
    :return: callable
    """
    return lambda x: fun_f(fun_g(x))


def uncurry(fun_f):
    """
    Transform a function into a function taking one pair argument.

    :param fun_f: function taking two arguments
    :return: function taking one pair argument
    """
    return lambda pair: fun_f(pair[0], pair[1])


def curry(fun_f):
    """
    Transform a function into a function that takes as input two arguments.

    :param fun_f: function taking a pair as argument
    :return: function taking two arguments
    """
    return lambda x, y: fun_f((x, y))


def one(_):
    """
    Return always 1.

    :param _: anything
    :return: 1
    """
    return 1


def zero(_):
    """
    Return always 0.

    :param _: anything
    :return: 0
    """
    return 0


def add(*args):
    """
    Generalized addition.

    :param args: list
        A list of numbers
    :return: number
    """
    return functools.reduce(operator.add, args, 0)


def incr(num):
    """
    Increment its argument by 1.

    :param num: number
    :return: number
    """
    return num + 1


def decr(num):
    """
    Decrement its argument by 1.

    :param num: number
    :return: number
    """
    return num - 1


def is_even(num):
    """
    Check whether its argument is even.

        >>> is_even(2)
        True
        >>> is_even(3)
        False

    :param num: int
    :return: bool
    """
    return num % 2 == 0


def is_odd(num):
    """
    Check whether its argument is odd.

        >>> is_odd(2)
        False
        >>> is_odd(3)
        True

    :param num: int
    :return: bool
    """
    return num % 2 == 1
