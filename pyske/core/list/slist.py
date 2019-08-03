"""
A module of sequential lists and associated primitives

class SList: sequential lists.
"""
import functools
from operator import concat
from typing import TypeVar, Callable, Sequence, Tuple, Optional, Generic
from pyske.core import interface
from pyske.core.support.list import scan

__all__ = ['SList']

T = TypeVar('T')  # pylint: disable=invalid-name
R = TypeVar('R')  # pylint: disable=invalid-name
U = TypeVar('U')  # pylint: disable=invalid-name


class SList(list, interface.List, Generic[T]):
    # pylint: disable=too-many-public-methods
    """
    Sequential list.

    Static methods from interface IList:
        init, from_seq.

    Methods from interface IList:
        length, to_seq,
        map, mapi, map2, map2i, zip, filter,
        reduce, map_reduce, scanl, scanl_last, scanr,
        get_partition, flatten,
        distribute, balance,
        gather, scatter, scatter_range,
        invariant.

    Static methods:
        from_str.

    Methods:
        head, tail, empty,
        scanp.
    """

    @staticmethod
    def from_str(string: str, parser: Callable[[str], U] = int,
                 opening: str = "[", closing: str = "]", separator: str = ",") -> 'SList[T]':
        """
        Create a list from a string.

        :param string:
            A string representation of the list.
        :param parser: (default: `ìnt``)
            A function that transforms a string into a value of a specific type.
        :param opening: (default: '['):
            The opening string in the string representation of the list.
        :param closing: (default: ']'):
            The closing string in the string representation of the list.
        :param separator: (default: ','):
            The separator string in the string representation of the list.
        """
        res = SList([])
        values = string.replace(opening, "").replace(closing, "").split(separator)
        for val in values:
            res.append(parser(val))
        return res

    def head(self):
        """Gives the first element of the current instance"""
        if self.empty():
            return None
        return self[0]

    def tail(self):
        """Gives the the current instance without its first element"""
        return SList(self[1:])

    def empty(self):
        """Indicates if a list is empty"""
        return self.length() == 0

    @staticmethod
    def init(value_at: Callable[[int], T], size: int) -> 'SList[T]':
        assert size >= 0
        return SList([value_at(i) for i in range(0, size)])

    def length(self: 'SList[T]') -> int:
        return len(self)

    def filter(self: 'SList[T]', predicate: Callable[[T], bool]):
        return SList(filter(predicate, self))

    def map(self: 'SList[T]', unary_op: Callable[[T], R]) -> 'SList[R]':
        return SList(map(unary_op, self))

    def mapi(self: 'SList[T]', binary_op: Callable[[int, T], R]) -> 'SList[R]':
        return SList([binary_op(i, self[i]) for i in range(0, len(self))])

    def map_reduce(self: 'SList[T]', unary_op: Callable[[T], R],
                   binary_op: Callable[[R, R], R], neutral: Optional[T] = None) -> R:
        if self.empty():
            return neutral
        if neutral is None:
            return functools.reduce(binary_op, map(unary_op, self))
        return functools.reduce(binary_op, map(unary_op, self), neutral)

    def reduce(self: 'SList[T]', binary_op: Callable[[T, T], T], neutral: Optional[T] = None) -> T:
        if neutral is None:
            return functools.reduce(binary_op, self)
        return functools.reduce(binary_op, self, neutral)

    def scanl(self: 'SList[T]', binary_op: Callable[[R, T], R], neutral: R) -> 'SList[R]':
        res = self.copy()
        for (idx, value) in enumerate(res):
            res[idx] = neutral
            neutral = binary_op(neutral, value)
        return SList(res)

    def scanr(self: 'SList[T]', binary_op: Callable[[R, T], R]) -> 'SList[R]':
        assert self != []
        res = self.copy()
        acc = res[0]
        for idx in range(1, len(res)):
            acc = binary_op(acc, self[idx])
            res[idx] = acc
        return SList(res)

    def scanl_last(self: 'SList[T]', binary_op: Callable[[R, T], R], neutral: R)\
            -> 'Tuple[SList[R], R]':
        res = scan(self, binary_op, neutral)
        last: R = res.pop()
        return res, last

    def scanp(self: 'SList[T]', binary_op, neutral):
        """
        Makes a leftward accumulation of the values from an neutral one.
        The result of scanp is a list of size n where n is the size of self
        and one additional value corresponding to the total accumulation.

        Definition:
            scanp f c [x_1, x_2, ..., x_n] = [f(x_2, f(x_3, f(..., c))), ..., f(x_n, c), c]

        Parameters
        ----------
        binary_op : callable
            A function to make a new accumulation from the previous accumulation and a current value
            Usually, f is associative.
        neutral
            neutral value for the accumulator.
            Usually, c is the unit of f, i.e. f(value, c) = f(c, value) = value
        """
        res = self.copy()
        for idx in range(len(self), 0, -1):
            res[idx - 1] = neutral
            neutral = binary_op(self[idx - 1], neutral)
        return res

    def zip(self: 'SList[T]', a_list: 'SList[U]') -> 'SList[Tuple[T, U]]':
        assert len(self) == len(a_list)
        a_list: Sequence[Tuple[T, U]] = [(left, right) for (left, right) in zip(self, a_list)]
        return SList(a_list)

    def map2(self: 'SList[T]', binary_op: Callable[[T, U], R], a_list: 'SList[U]') -> 'SList[R]':
        assert len(self) == len(a_list)
        return SList([binary_op(left, right) for (left, right) in zip(self, a_list)])

    def map2i(self: 'SList[T]', ternary_op: Callable[[int, T, U], R],
              a_list: 'SList[U]') -> 'SList[R]':
        assert len(self) == len(a_list)
        return SList([ternary_op(i, self[i], a_list[i]) for i in range(0, len(self))])

    def get_partition(self: 'SList[T]') -> 'SList[SList[T]]':
        return SList([self])

    def flatten(self: 'SList[SList[T]]',
                new_distr: interface.Distribution = None) -> 'SList[T]':
        a_list = functools.reduce(concat, self, [])
        return SList(a_list)

    def distribute(self: 'SList[T]', _: interface.Distribution) -> 'SList[T]':
        return self

    def balance(self: 'SList[T]') -> 'SList[T]':
        return self

    @staticmethod
    def from_seq(sequence: Sequence[T]) -> 'SList[T]':
        return SList(sequence)

    def to_seq(self: 'SList[T]') -> 'SList[T]':
        return self

    def gather(self: 'SList[T]', pid: int) -> 'SList[T]':
        assert pid == 0
        return self

    def invariant(self: 'SList[T]') -> bool:
        return True

    def scatter(self: 'SList[T]', pid: int) -> 'SList[T]':
        assert pid == 0
        return self

    def scatter_range(self: 'SList[T]', rng: range) -> 'SList[T]':
        return self[rng.start:rng.stop:rng.step]

    def permute(self: 'SList[T]', bij: Callable[[int], int]) -> 'SList[T]':
        a_list = self.copy()
        for (idx, value) in enumerate(self):
            a_list[bij(idx)] = value
        return SList(a_list)
