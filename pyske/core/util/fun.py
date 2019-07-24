__all__ = ['idt', 'compose', 'curry', 'uncurry', 'zero', 'one', 'add', 'incr', 'decr']

import functools
import operator


def idt(x):
    return x


def compose(f, g):
    return lambda x: f(g(x))


def uncurry(f):
    return lambda pair: f(pair[0], pair[1])


def curry(f):
    return lambda x, y: f((x, y))


def one(_):
    return 1


def zero(_):
    return 0


def add(*args):
    return functools.reduce(operator.add, args, 0)


def incr(x):
    return x + 1


def decr(x):
    return x - 1
