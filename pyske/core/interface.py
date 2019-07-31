"""
linear: interface for PySke linearly ordered data structures.

Interfaces: Distribution, List.
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Optional, Sequence, Tuple, Any

__all__ = ['List', 'Distribution']

T = TypeVar('T')  # pylint: disable=invalid-name
U = TypeVar('U')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name


class Distribution(ABC, list):
    """
    A class to represent the distribution of parallel linear data structure.
    """

    @abstractmethod
    def is_valid(self, size: int) -> bool:
        """
        Check if the distribution is valid.

        Checks if the current distribution really represent the distribution
        a of linear structure of the given size. Each element of the distribution
        should be positive, its length should be equal to the number of
        available processors, and the sum of all its elements should be
        equal to the given size.

        :param size: should be >= 0
        :return: bool
        """

    @staticmethod
    @abstractmethod
    def balanced(size: int) -> 'Distribution':
        """
        Return a balanced distribution.

        :param size: should be >= 0
        :return: Returns a balanced distribution, i.e. a distribution
        such that for any two elements, their differ by at most 1.
        The sum of all the elements is size.
        """

    @abstractmethod
    def to_pid(self, index: int, value) -> Tuple[int, Tuple[int, Any]]:
        """
        Return the processor identifier of the given index.

        :param index: a valid index
        :param value: a value
        :return: a processor identifier
        """


class List(ABC, Generic[T]):
    # pylint: disable=too-many-public-methods
    """
    PySke lists (interface)

    Static methods:
        init, from_seq.

    Methods:
        length, to_seq,
        map, mapi, map2, map2i, zip, filter,
        reduce, map_reduce, scanl, scanl_last, scanr,
        get_partition, flatten,
        distribute, balance,
        gather, scatter, scatter_range,
        invariant.
    """

    @abstractmethod
    def __init__(self):
        """
        Return an empty list.
        """

    @staticmethod
    @abstractmethod
    def init(value_at, size):
        """
        Return a list built using a function.

        Example::

            >>> from pyske.core.list.slist import SList
            >>> SList.init(str, 3)
            ['0', '1', '2']

        :param value_at: unary function
        :param size: size >= 0
        :return: a list of the given size, where for all valid index
            i, the value at this index is value_at(i)
        """

    @abstractmethod
    def __len__(self) -> int:
        """
        Return the length of the list.

        :return: the global length of the list.
        """

    @staticmethod
    @abstractmethod
    def from_seq(sequence: Sequence[T]) -> 'List[T]':
        """
        Return a list built from a sequential list at processor 0.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> from pyske.core.util import par
            >>> SList.from_seq([1, 2, 3])
            [1, 2, 3]
            >>> PList.from_seq([1, 2, 3]).to_seq()
            [1, 2, 3]
            >>> PList.from_seq([1, 2, 3]).get_partition().map(len).to_seq() == \
                    [3 if pid == 0 else 0 for pid in par.procs()]
            True

       :param sequence: a list (at processor 0).
       :return: a list with the same content, all at processor 0.
       """

    def to_seq(self: 'List[T]') -> 'List[T]':
        """
        Return a sequential list with same content.

        Example::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList.init(float, 4).to_seq()
            [0.0, 1.0, 2.0, 3.0]
            >>> PList.init(float, 4).to_seq()
            [0.0, 1.0, 2.0, 3.0]

        :return: a sequential list.
        """

    @abstractmethod
    def length(self) -> int:
        """
        Return the length of the list.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList().length()
            0
            >>> PList.init(lambda x: x, 3).length()
            3

        :return: the global length of the list.
        """

    @abstractmethod
    def invariant(self) -> bool:
        """
        Check that the class invariant holds.

        :return: True is the invariant holds, False otherwise.
        """

    @abstractmethod
    def map(self: 'List[T]', unary_op: Callable[[T], V]) -> 'List[V]':
        """
        Apply a function to all the elements.

        The returned list has the same shape (same length, same distribution)
        than the initial list.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList.init(lambda x: x, 5).map(str)
            ['0', '1', '2', '3', '4']
            >>> PList.init(lambda x:x, 3).map(lambda x: x + 1).to_seq()
            [1, 2, 3]

        :param unary_op: function to apply to elements
        :return: a new list
        """

    @abstractmethod
    def mapi(self: 'List[T]', binary_op: Callable[[int, T], V]) -> 'List[V]':
        """
        Apply a function to all the elements and their indices.

        The returned list has the same shape (same length, same distribution)
        than the initial list.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList.init(lambda x: x, 5).mapi(lambda i, x: i * x)
            [0, 1, 4, 9, 16]
            >>> PList.init(lambda x: x, 5).mapi(lambda i, x: i * x).to_seq()
            [0, 1, 4, 9, 16]

        :param binary_op: function to apply to each index and element
        :return: a new list
        """

    @abstractmethod
    def map2(self: 'List[T]', binary_op: Callable[[T, U], V],
             a_list: 'List[U]') -> 'List[V]':
        """
        Apply a function to all the elements of ``self`` and ``sequence``.

        The returned list has the same shape (same length, same distribution)
        than the initial lists.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList

            >>> l = SList.init(lambda x: 5-x, 5)
            >>> SList.init(lambda x: x, 5).map2(lambda x, y: x + y, l)
            [5, 5, 5, 5, 5]
            >>> l = PList.init(lambda x: 5-x, 5)
            >>> PList.init(lambda x: x, 5).map2(lambda x, y: x + y, l).to_seq()
            [5, 5, 5, 5, 5]

        :param binary_op: function to apply to each pair of elements
        :param a_list: the second list.
            The length of ``sequence`` should be the same than the length of ``self``.
        :return: a new list.
        """

    @abstractmethod
    def map2i(self: 'List[T]', ternary_op: Callable[[int, T, U], V],
              a_list: 'List[U]') -> 'List[V]':
        """
        Apply a function to all the indices and elements of both lists.

        The returned list has the same shape (same length, same distribution)
        than the initial lists.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> l = SList.init(lambda x: 5-x, 5)
            >>> SList.init(lambda x: x, 5).map2i(lambda i, x, y: i*(x + y), l)
            [0, 5, 10, 15, 20]
            >>> l = PList.init(lambda x: 5-x, 5)
            >>> PList.init(lambda x: x, 5).map2i(lambda i, x, y: i*(x + y), l).to_seq()
            [0, 5, 10, 15, 20]

        :param ternary_op: function to apply to each index, and elements of both lists.
        :param a_list: the second list.
        :return: a new list.
        """

    @abstractmethod
    def zip(self: 'List[T]', a_list: 'List[U]') -> 'List[Tuple[T, U]]':
        """
        Create a list of pairs.

        The returned list has the same shape (same length, same distribution)
        than the initial lists.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> l = SList.init(float, 4)
            >>> l.zip(l)
            [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]
            >>> l = PList.init(str, 2)
            >>> l.zip(l).to_seq()
            [('0', '0'), ('1', '1')]

        :param a_list: a list of same shape than ``self``.
        :return: a list of pairs.
        """

    @abstractmethod
    def filter(self: 'List[T]', predicate: Callable[[T], bool]) -> 'List[T]':
        """
        Return a filtered list.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList.init(lambda x: x, 4).filter(lambda x: x % 2 == 0)
            [0, 2]
            >>> PList.init(lambda x: x, 4).filter(lambda x: x % 2 == 0).to_seq()
            [0, 2]

        :param predicate:
            the elements in the output satisfy this predicate.
        :return: a new list.
        """

    @abstractmethod
    def get_partition(self: 'List[T]') -> 'List[List[T]]':
        """
        Make the distribution visible.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> from pyske.core.util import par
            >>> SList.init(int, 4).get_partition()
            [[0, 1, 2, 3]]
            >>> PList.init(float, 4).get_partition().to_seq() \
                    if par.procs() == [0, 1] else [[0, 1], [2, 3]]
            [[0, 1], [2, 3]]

        :return: a list of lists.
        """

    @abstractmethod
    def flatten(self: 'List[List[T]]') -> 'List[T]':
        """
        Flatten the list of lists.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList([[0], [1, 2], [3, 4]]).flatten()
            [0, 1, 2, 3, 4]
            >>> PList.init(lambda i: list(range(0, i+1)), 3).flatten().to_seq()
            [0, 0, 1, 0, 1, 2]

        :return: a flattened list.
        """

    @abstractmethod
    def reduce(self: 'List[T]', binary_op: Callable[[T, T], T], neutral: Optional[T] = None) -> T:
        """
        Reduce a list of value to one value.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList([9, 10, 11, 12]).reduce(lambda x, y: x + y, 0)
            42
            >>> SList().reduce(lambda x, y: x+y, [])
            []
            >>> PList.init(float, 4).reduce(lambda x, y: x + y)
            6.0

        :param binary_op: a binary associative  operation
        :param neutral: (optional):
            a value that should be a neutral element for the operation,
            i.e. for all element e,
                ``binary_op(neutral, e) == binary_op(e, neutral) == e``.
            If this argument is omitted the list should not be empty.
        :return: a value
        """

    @abstractmethod
    def map_reduce(self: 'List[T]', unary_op: Callable[[T], V],
                   binary_op: Callable[[V, V], V], neutral: Optional[V] = None) -> V:
        """
        Combination of a map and a reduce.

        Examples::
            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList([8, 9, 10, 11]).map_reduce(lambda x: x + 1, lambda x, y: x + y)
            42
            >>> PList.init(float, 4).map_reduce(lambda x: x + 1, lambda x, y: x * y)
            24.0

        :param unary_op: unary operation.
        :param binary_op: binary associative  operation.
        :param neutral: (optional) neutral element for the binary operation.
             i.e. for all element e,
                ``binary_op(neutral, e) == binary_op(e, neutral) == e``.
             If this argument is omitted the list should not be empty.
        :return: a value.
        """

    @abstractmethod
    def scanr(self: 'List[T]', binary_op: Callable[[T, T], T]) -> 'List[T]':
        """
        Return the prefix-sum from right-to-left.

        The list should not be empty.
        The returned list has the same shape (same length, same distribution)
        than the initial list.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList.init(float, 4).scanr(lambda x, y: x + y)
            [0.0, 1.0, 3.0, 6.0]
            >>> PList.init(str, 4).scanr(lambda x, y: x + y).to_seq()
            ['0', '01', '012', '0123']

        :param binary_op: a binary associative  operation.
        :return: a new list.
        """

    @abstractmethod
    def scanl_last(self: 'List[T]', binary_op: Callable[[T, T], T], neutral: T):
        """
        Return the prefix-sum list and the reduction.

        The first element is always ``neutral``.
        The returned list has the same shape (same length, same distribution)
        than the initial list.

        [x_1, ..., x_n].scanl(op, e) == [e, op(e, x_1), ..., op(..(op(e, x1), ...), x_n)]

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList.init(float, 4).scanl_last(lambda x, y: x + y, 0.0)
            ([0.0, 0.0, 1.0, 3.0], 6.0)
            >>> (sequence, value) = PList.init(lambda x: x + 1, 4).scanl_last(lambda x, y: x + y, 0)
            >>> (sequence.to_seq(), value)
            ([0, 1, 3, 6], 10)

        :param binary_op: a binary associative  operation.
        :param neutral: the neutral element for the binary operation.
            i.e. for all element e,
                ``binary_op(neutral, e) == binary_op(e, neutral) == e``.
            If this argument is omitted the list should not be empty.
        :return: a new list and a value.
        """

    @abstractmethod
    def scanl(self: 'List[T]', binary_op: Callable[[T, T], T], neutral: T) -> 'List[T]':
        """
        Return the prefix-sum list.

        The first element is always ``neutral``.
        The returned list has the same shape (same length, same distribution)
        than the initial list.

        [x_1, ..., x_n].scanl(op, e) == [e, op(e, x_1), ..., op(..(op(e, x1), ...), x_n)]

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> SList.init(float, 4).scanl(lambda x, y: x + y, 0.0)
            [0.0, 0.0, 1.0, 3.0]
            >>> PList.init(lambda x: x + 1, 4).scanl(lambda x, y: x + y, 0).to_seq()
            [0, 1, 3, 6]

        :param binary_op: a binary associative  operation.
        :param neutral: the neutral element for the binary operation.
            i.e. for all element e,
                ``binary_op(neutral, e) == binary_op(e, neutral) == e``.
            If this argument is omitted the list should not be empty.
        :return: a new list.
        """

    @abstractmethod
    def distribute(self: 'List[T]', target_distr: Distribution) -> 'List[T]':
        """
        Copy the list while changing its distribution.

        In sequential, it just returns ``self``. In parallel, communications
        are performed to meet the new distribution.

        Examples::

            >>> from pyske.core.list.slist import SList
            >>> from pyske.core.list.plist import PList
            >>> from pyske.core.util import par
            >>> distr = [4 if pid == 0 else 0 for pid in par.procs()]
            >>> SList.init(int, 4).distribute(distr)
            [0, 1, 2, 3]
            >>> PList.init(int, 4).distribute(distr).get_partition().to_seq() == \
                    [list(range(0,4)) if index == 0 else [] for index in par.procs()]
            True

        :param target_distr: a list of positive numbers.
            The sum of this list should be the length of ```self``.
        :return: a list containing the same elements.
        """

    @abstractmethod
    def balance(self: 'List[T]') -> 'List[T]':
        """
        Copy the list while changing its distribution.

        In sequential, it just returns ``self``. In parallel, communications
        are performed so that the list is evenly distributed.

            >>> from pyske.core import SList, PList, Distribution
            >>> from pyske.core.util import par

            >>> SList.init(int, 4).balance()
            [0, 1, 2, 3]
            >>> PList.init(int, 4).balance().get_partition().map(len).to_seq() == \
                    Distribution.balanced(4)
            True

        :return: a list containing the same elements.
        """

    @abstractmethod
    def gather(self: 'List[T]', pid: int) -> 'List[T]':
        """
        Gather all the elements on one processor.

        In sequential, it returns ``self``.
        In parallel, all the content is gathered at the given
        processor. The content remains the same.

        Examples::

            >>> from pyske.core import SList, PList
            >>> from pyske.core.util import par

            >>> SList.init(int, 4).gather(0)
            [0, 1, 2, 3]
            >>> lst1 = PList.init(int, 4).gather(0).get_partition().to_seq()
            >>> lst2 = PList.from_seq([0, 1, 2, 3]).get_partition().to_seq()
            >>> lst1 == lst2
            True

        The content of the list remains unchanged.

        :param pid: should be a valid processor.
            ```id in par.procs()``
        :return: same content but all the elements on processor ``pid``.
        """

    @abstractmethod
    def scatter(self: 'List[T]', pid: int) -> 'List[T]':
        """
        Return a new list containing elements from processor ``pid``.

        Examples::

            >>> from pyske.core import SList, PList, Distribution, par
            >>> SList.init(str, 3).scatter(0)
            ['0', '1', '2']
            >>> PList.from_seq([1, 2, 3]).scatter(0).get_partition().map(len).to_seq() == \
                    Distribution.balanced(3)
            True

        :param pid: should be a valid processor.
            ```id in par.procs()``
        :return: a list of size the content of ``self``at processor ``pid``.
        """

    @abstractmethod
    def scatter_range(self: 'List[T]', rng) -> 'List[T]':
        """
        Return a new list containing elements in the range.

        In sequential, is equivalence to slice from a range.
        In parallel, the resulting list is evenly distributed.

        Examples::

            >>> from pyske.core import SList, PList, Distribution, par
            >>> SList.init(str, 3).scatter(0)
            ['0', '1', '2']
            >>> PList.from_seq(SList.init(int, 10)).scatter_range(range(0,3)) \
                    .get_partition().map(len).to_seq() \
                    == Distribution.balanced(3)
            True

        :param rng: a valid range.
        :return: a new list containing the elements in the range.
        """

    @abstractmethod
    def permute(self: 'List[T]', bij: Callable[[int], int]) -> 'List[T]':
        """
        Permute the content of the list.

        Examples::

            >>> from pyske.core import SList, PList
            >>> SList.init(int, 7).permute(lambda i: 6-i)
            [6, 5, 4, 3, 2, 1, 0]
            >>> PList.init(int, 7).permute(lambda i: 6-i).to_seq()
            [6, 5, 4, 3, 2, 1, 0]

        :param bij: bijective function on list indices
        :return: same content but different ordering
        """
