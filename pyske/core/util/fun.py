"""
A module of useful simple functions.
"""
__all__ = ['idt', 'compose', 'curry', 'uncurry', 'zero', 'one', 'add', 'incr', 'decr']

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
    Transforms a function taking as two arguments into
    a function that takes one argument that is a pair.
    :param fun_f: callable
    :return: callable
    """
    return lambda pair: fun_f(pair[0], pair[1])


def curry(fun_f):
    """
    Transforms a function taking as argument a pair, into
    a function that takes as input two arguments.
    :param fun_f:
    :return:
    """
    return lambda x, y: fun_f((x, y))


def one(_):
    """
    Constant function that returns always 1.
    :param _: anything
    :return: 1
    """
    return 1


def zero(_):
    """
    Constant function that returns always 0.
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
    Increments its argument by 1.
    :param num: number
    :return: number
    """
    return num + 1


def decr(num):
    """
    Decrements its argument by 1.
    :param num: number
    :return: number
    """
    return num - 1
