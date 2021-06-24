"""
A module of sequential arrays and associated skeletons

class SArray2D: sequential arrays.
"""
import functools
from typing import TypeVar, Generic, Callable, Optional

# pylint: disable=unused-import
from pyske.core import SList
from pyske.core.array.array_interface import Array2D, Distribution

T = TypeVar('T')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name


class SArray2D(Array2D, Generic[T]):
    """
    Sequential arrays

    Static methods from interface IArray:
        init.

    Methods from interface IArray:
        map,reduce,
        get_partition,distribute

    """

    def __init__(self, content=None, line_size=-1, col_size=-1):
        super().__init__()
        if content is None:
            content = []
        self.__line_size = line_size
        self.__column_size = col_size
        self.__values = content

    @property
    def values(self):
        return self.__values

    @property
    def line_size(self):
        return self.__line_size

    @property
    def column_size(self):
        return self.__column_size

    def __str__(self):
        content = ""
        for i in range(self.__line_size):
            content += "("
            for j in range(self.__column_size):
                content += '%4s' % self.__values[i * self.__column_size + j]
            content += '%4s' % ')'
            if i != self.line_size - 1:
                content += '\n'
        return content

    def __repr__(self):
        return str(self)

    def __len__(self):
        return self.__column_size * self.__line_size

    @staticmethod
    def init(value_at: Callable[[int, int], V], _: Distribution, col_size: int,
             line_size: int) -> 'SArray2D[V]':
        assert col_size > 0
        assert line_size > 0
        content = []
        for line in range(line_size):
            for column in range(col_size):
                content.append(value_at(line, column))
        sarray2d = SArray2D(content, line_size, col_size)
        return sarray2d

    def map(self: 'SArray2D[T]', unary_op: Callable[[T], V]) -> 'SArray2D[V]':
        content = list(map(unary_op, self.__values))
        return SArray2D(content, self.__line_size, self.__column_size)

    def reduce(self: 'SArray2D[T]', binary_op: Callable[[T, T], T],
               neutral: Optional[T] = None) -> T:
        if neutral is None:
            return functools.reduce(binary_op, self.__values)
        return functools.reduce(binary_op, self.__values, neutral)

    def get_partition(self: 'SArray2D[T]') -> 'SList[SArray2D[T]]':
        return SList([self])

    def distribute(self: 'SArray2D[T]') -> 'SArray2D[T]':
        return self
