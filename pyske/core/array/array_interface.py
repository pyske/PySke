"""
Interface for PySke array.

Interfaces: Array2D.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Generic, TypeVar, Optional

# pylint: disable=unused-import
from pyske.core.interface import List
from pyske.core.support import parallel as parimpl

T = TypeVar('T')  # pylint: disable=invalid-name
U = TypeVar('U')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name

_PID: int = parimpl.PID
_NPROCS: int = parimpl.NPROCS
_COMM = parimpl.COMM

class Distribution(Enum):
    LINE = 'LINE'
    COLUMN = 'COLUMN'

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
        Return an empty array.
        """

    @staticmethod
    @abstractmethod
    def init(value_at: Callable[[int, int], V], distribution: Distribution, col_size: int,
             line_size: int) -> 'Array2D[V]':
        """
        Return an array built using a function

        Example::

            >>> from pyske.core.array.sarray2d import SArray2D
            >>> from pyske.core.array.array_interface import Distribution
            >>> number_line = 2
            >>> number_column = 2
            >>> init_function = lambda line, column: line * number_column + column
            >>> SArray2D.init(init_function, Distribution.LINE, number_column, number_line)
            (   0   1   )
            (   2   3   )

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
        are performed to meet line or column distribution.

        Examples::

            >>> from pyske.core.array.sarray2d import SArray2D
            >>> from pyske.core.array.array_interface import Distribution
            >>> sarray2d = SArray2D.init(lambda i, j: 1, Distribution.LINE, col_size=2, line_size=2)
            >>> sarray2d.distribute()
            (   1   1   )
            (   1   1   )

        :return: an array containing the same elements.
        """

    @abstractmethod
    def map(self: 'Array2D[T]', unary_op: Callable[[T], V]) -> 'Array2D[V]':
        """
        Apply a function to all the elements.

        The returned array has the same shape (same size, same distribution)
        than the initial array.

        Examples::

            >>> from pyske.core.array.sarray2d import SArray2D
            >>> from pyske.core.array.parray2d import PArray2D
            >>> from pyske.core.array.array_interface import Distribution
            >>> col_size = 2
            >>> line_size = 2
            >>> SArray2D.init(lambda i, j: 1, Distribution.LINE, col_size, line_size).map(lambda x: x + 1)
            (   2   2   )
            (   2   2   )
            >>> parray2d = PArray2D.init(lambda i, j: 1, Distribution.LINE, col_size=2, line_size=2).map(lambda x: x + 1)
            >>> parray2d.to_seq()
            (   2   2   )
            (   2   2   )

        :param unary_op: function to apply to elements
        :return: a new array
        """

    @abstractmethod
    def reduce(self: 'Array2D[T]', binary_op: Callable[[T, T], T],
               neutral: Optional[T] = None) -> T:
        """
        Reduce an array of value to one value.

        Examples::

            >>> from pyske.core.array.sarray2d import SArray2D
            >>> from pyske.core.array.parray2d import PArray2D
            >>> from pyske.core.array.array_interface import Distribution
            >>> parray2d = PArray2D.init(lambda i, j: 1, Distribution.COLUMN, col_size=2, line_size=2)
            >>> parray2d.reduce(lambda x, y: x + y)
            4
            >>> SArray2D().reduce(lambda x, y: x + y, 0)
            0

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

        Examples::

            >>> from pyske.core.array.sarray2d import SArray2D
            >>> from pyske.core.array.parray2d import PArray2D
            >>> from pyske.core.array.array_interface import Distribution
            >>> from pyske.core.util import par
            >>> col_size = 2
            >>> line_size = 2
            >>> init_function = lambda line, column: line * col_size + column
            >>> SArray2D.init(init_function, Distribution.LINE, col_size, line_size).get_partition()
            [(   0   1   )
            (   2   3   )]
            >>> parray2d = PArray2D.init(init_function, Distribution.LINE, col_size=2, line_size=2)
            >>> parray2d.get_partition().to_seq() if par.procs() == [0, 1] else '[(   0   1   ), (   2   3   )]'
            '[(   0   1   ), (   2   3   )]'

        :return: a list of array.
        """

    @abstractmethod
    def map2(self: 'Array2D[T]', binary_op: Callable[[T, U], V],
             a_array: 'Array2D[U]') -> 'Array2D[V]':
        """
        Apply a function to all the elements of ``self`` and an array.

        The returned array has the same shape (same size, same distribution)
        than the initial arrays.

        Examples::

            >>> from pyske.core.array.sarray2d import SArray2D
            >>> from pyske.core.array.array_interface import Distribution
            >>> sarray2d = SArray2D.init(lambda line, column: 1, Distribution.LINE, col_size = 2, line_size = 2)
            >>> sarray2d.map2(lambda x, y: x + y, sarray2d)
            (   2   2   )
            (   2   2   )

        :param binary_op: function to apply to each pair of elements
        :param a_array: the second array.
            The second array must have same column and line size than `self`.
        :return: a new array.
        """

    @abstractmethod
    def to_seq(self: 'Array2D[T]') -> 'Array2D[T]':
        """
        Return a sequential array with same content.

        The distribution must be per line.

        Examples::

            >>> from pyske.core.array.sarray2d import SArray2D
            >>> from pyske.core.array.parray2d import PArray2D
            >>> from pyske.core.array.array_interface import Distribution
            >>> PArray2D.init(lambda i, j: 1, Distribution.LINE, col_size=2, line_size=2).to_seq()
            (   1   1   )
            (   1   1   )
            >>> SArray2D.init(lambda line, column: 1, Distribution.LINE, col_size = 2, line_size = 2).to_seq()
            (   1   1   )
            (   1   1   )

        :return: a sequential array.
        """
