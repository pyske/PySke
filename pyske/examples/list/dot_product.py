"""
Dot product of two vectors implemented as parallel lists
"""

from operator import add, mul
from pyske.core.util import fun

__all__ = ['opt_dot_product', 'dot_product']


# ------------------- Dot Product Variant Example -------------


def dot_product(vector1, vector2):
    """
    Compute the dot product of two vectors.

    :param vector1: list of numbers representing a vector
    :param vector2: list of numbers representing a vector
    :return: the dot product of the two vectors
    """
    return vector1.map2(mul, vector2).reduce(add, 0)


# ------------------- Dot Product Example -------------------


def opt_dot_product(vector1, vector2, uncurry=fun.uncurry):
    """
    Compute the dot product of two vectors.

    :param vector1: list of numbers representing a vector
    :param vector2: list of numbers representing a vector
    :param uncurry: (optional)
    :return: the dot product of the two vectors

    Examples::

        >>> from pyske.core import PList
        >>> vector_1 = PList.init(lambda x: x, 10)
        >>> vector_2 = PList.init(lambda x: 1, 10)
        >>> dot_product(vector_1, vector_2)
        45

        >>> from pyske.core import PList
        >>> vector_1 = PList.init(lambda x: x, 10)
        >>> vector_2 = PList.init(lambda x: 9 - x, 10)
        >>> dot_product(vector_1, vector_2)
        120

    """
    return vector1.zip(vector2).map(uncurry(mul)).reduce(add, 0)
