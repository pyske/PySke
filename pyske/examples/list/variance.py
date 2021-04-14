"""
Variance Example
"""
from operator import add

__all__ = ['variance']


# ------------------- Variance of a Random Variable ----------------------

def variance(input_list):
    """
    Return the variance of a random variable.

    :param input_list: a PySke list of numbers
    :return a number: the variance
    """
    size = input_list.length()
    avg = input_list.reduce(add) / size
    var = input_list.map(lambda num: (num - avg) ** 2).reduce(add) / size
    return var


# ---------------------- Execution -----------------------

if __name__ == '__main__':
    from pyske.examples.list.util import standard_main
    standard_main(variance)
