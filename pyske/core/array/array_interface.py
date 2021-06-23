"""
Interface for PySke array.

Interfaces: Array2D.
"""

from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar, Optional

from pyske.core.array.parray2d import Distribution
# pylint: disable=unused-import
from pyske.core.interface import List
from pyske.core.support import parallel as parimpl

T = TypeVar('T')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name

_PID: int = parimpl.PID
_NPROCS: int = parimpl.NPROCS
_COMM = parimpl.COMM

class Array2D(ABC, Generic[T]):
    """
        PySke array2d (interface)

        Static methods:
            init.

        Methods:
            map, reduce, distribute,
            get_partition.
        """

    @abstractmethod
    def __init__(self: 'Array2D[T]') -> None:
        """
        Return an empty list.
        """

    @staticmethod
    @abstractmethod
    def init(value_at: Callable[[int, int], V], distribution: Distribution,
             col_size: int = _NPROCS,
             line_size: int = _NPROCS) -> 'Array2D[V]':
        """
        Return an array built using a function per line on each processor

        :param value_at: binary function
        :param distribution: the distribution direction (LINE, COLUMN)
        :param col_size: number of columns
        :param line_size: number of lines
        :return: an 2d array of the given line and column size, where for all valid line column
            i, j, the value at this index is value_at(i, j)
        """

    @abstractmethod
    def distribute(self: 'Array2D[T]') -> 'Array2D[T]':
        """
        Copy the array while changing its distribution.

        In sequential, it just returns ``self``. In parallel, communications
        are performed to meet the new distribution.

        :return: an array containing the same elements.
        """

    @abstractmethod
    def map(self: 'Array2D[T]', unary_op: Callable[[T], V]) -> 'Array2D[V]':
        """
        Apply a function to all the elements.

        The returned array has the same shape (same size, same distribution)
        than the initial array.

        :param unary_op: function to apply to elements
        :return: a new array
        """

    @abstractmethod
    def reduce(self: 'PArray2D[T]', binary_op: Callable[[T, T], T],
               neutral: Optional[T] = None) -> T:
        """
        Reduce an array of value to one value.

        :param binary_op: a binary associative and commutative operation
        :param neutral: (optional):
            a value that should be a neutral element for the operation,
            i.e. for all element e,
                ``binary_op(neutral, e) == binary_op(e, neutral) == e``.
            If this argument is omitted the list should not be empty.
        :return: a value
        """

    @abstractmethod
    def get_partition(self: 'Array2D[T]') -> 'List[Array2D[T]]':
        """
        Make the distribution visible.

        :return: a list of array.
        """
