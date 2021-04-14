"""
A module of parallel lists and associated skeletons

class PList: parallel lists.
"""
import functools
from collections import defaultdict
from operator import add, concat
from typing import Optional, Tuple, Sequence, Generic  # pylint: disable=unused-import
from typing import TypeVar, Callable  # pylint: disable=unused-import

from pyske.core.list.slist import SList
from pyske.core.list.distribution import Distribution
from pyske.core import interface
from pyske.core.support import parallel as parimpl, interval
from pyske.core.support.list import scan
from pyske.core.util import par

__all__ = ['PList']

_PID: int = parimpl.PID
_NPROCS: int = parimpl.NPROCS
_COMM = parimpl.COMM

T = TypeVar('T')  # pylint: disable=invalid-name
U = TypeVar('U')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name
R = TypeVar('R')  # pylint: disable=invalid-name

def _group_by(a_list):
    dic = defaultdict(list)
    for key, val in a_list:
        dic[key].append(val)
    return dic


class PList(interface.List, Generic[T]):
    # pylint: disable=too-many-public-methods
    # pylint: disable=protected-access
    """
    Distributed lists

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
    """
    __distribution: Distribution

    def __init__(self: 'PList[T]'):
        # pylint: disable=super-init-not-called
        self.__content: 'SList[T]' = SList([])
        self.__global_size: int = 0
        self.__local_size: int = 0
        self.__start_index: int = 0
        self.__distribution = Distribution([0 for _ in range(0, _NPROCS)])

    def __get_shape(self: 'PList[T]') -> 'PList':
        p_list = PList()
        p_list.__local_size = self.__local_size
        p_list.__global_size = self.__global_size
        p_list.__distribution = self.__distribution
        p_list.__start_index = self.__start_index
        return p_list

    def __str__(self: 'PList[T]') -> str:
        return "PID[" + str(_PID) + "]:\n" + \
               "  global_size: " + str(self.__global_size) + "\n" + \
               "  local_size: " + str(self.__local_size) + "\n" + \
               "  start_index: " + str(self.__start_index) + "\n" + \
               "  distribution: " + str(self.__distribution) + "\n" + \
               "  content: " + str(self.__content) + "\n"

    @property
    def distribution(self):
        """Return the distribution of the list"""
        return self.__distribution

    def invariant(self: 'PList[T]') -> None:
        assert isinstance(self.__content, SList)
        assert isinstance(self.__distribution, Distribution)
        prefix = scan(self.__distribution, add, 0)
        assert len(self.__content) == self.__local_size
        assert self.__distribution[_PID] == self.__local_size
        assert self.__start_index == prefix[_PID]
        assert prefix[_NPROCS] == self.__global_size

    def __len__(self) -> int:
        return self.__global_size

    def length(self: 'PList[T]') -> int:
        return self.__global_size

    @staticmethod
    def init(value_at: Callable[[int], T], size: int = _NPROCS) -> 'PList[T]':
        assert size >= 0
        p_list = PList()
        p_list.__global_size = size
        p_list.__local_size = parimpl.local_size(_PID, size)
        distribution_list = [parimpl.local_size(i, size) for i in range(0, _NPROCS)]
        p_list.__distribution = Distribution(distribution_list)
        p_list.__start_index = SList(p_list.__distribution).scanl(lambda x, y: x + y, 0)[_PID]
        p_list.__content = SList([value_at(i) for i in
                                  range(p_list.__start_index,
                                        p_list.__start_index + p_list.__local_size)])
        p_list.__distribution = [parimpl.local_size(i, size) for i in range(0, _NPROCS)]
        return p_list

    def map(self: 'PList[T]', unary_op: Callable[[T], V]) -> 'PList[V]':
        p_list = self.__get_shape()
        p_list.__content = self.__content.map(unary_op)
        return p_list

    def mapi(self: 'PList[T]', binary_op: Callable[[int, T], V]) -> 'PList[V]':
        p_list = self.__get_shape()
        p_list.__content = self.__content.mapi(lambda i, x: binary_op(i + self.__start_index, x))
        return p_list

    def map2(self: 'PList[T]', binary_op: Callable[[T, U], V], a_list: 'PList[U]') -> 'PList[V]':
        assert self.__distribution == a_list.__distribution
        res = self.__get_shape()
        res.__content = self.__content.map2(binary_op, a_list.__content)
        return res

    def map2i(self: 'PList[T]', ternary_op: Callable[[int, T, U], V],
              a_list: 'PList[U]') -> 'PList[V]':
        assert self.__distribution == a_list.__distribution
        res = self.__get_shape()
        res.__content = self.__content.map2i(lambda i, x, y:
                                             ternary_op(i + self.__start_index, x, y),
                                             a_list.__content)
        return res

    def map3(self: 'PList[T]', ternary_op: Callable[[T, U, V], R],
             a_list: 'PList[U]', b_list: 'PList[V]') -> 'PList[R]':
        assert self.__distribution == a_list.__distribution
        assert self.__distribution == b_list.__distribution
        res = self.__get_shape()
        res.__content = self.__content.map3(ternary_op, a_list.__content, b_list.__content)
        return res

    def zip(self: 'PList[T]', a_list: 'PList[U]') -> 'PList[Tuple[T, U]]':
        res = self.map2(lambda x, y: (x, y), a_list)
        return res

    def filter(self: 'PList[T]', predicate: Callable[[T], bool]) -> 'PList[T]':
        return self.get_partition().map(lambda l: l.filter(predicate)).flatten()

    def get_partition(self: 'PList[T]') -> 'PList[SList[T]]':
        p_list = PList()
        p_list.__content = SList([self.__content])
        p_list.__global_size = _NPROCS
        p_list.__local_size = 1
        p_list.__start_index = _PID
        p_list.__distribution = [1 for _ in par.procs()]
        return p_list

    def flatten(self: 'PList[SList[T]]', new_distr: Distribution = None) -> 'PList[T]':
        p_list = PList()
        p_list.__content = self.__content.flatten()
        p_list.__local_size = len(p_list.__content)
        if new_distr is None:
            p_list.__distribution = _COMM.allgather(p_list.__local_size)
        else:
            p_list.__distribution = new_distr
            assert new_distr[_PID] == p_list.__local_size
        p_list.__start_index = SList(p_list.__distribution).scanl(add, 0)[_PID]
        p_list.__global_size = SList(p_list.__distribution).reduce(add)
        return p_list

    def reduce(self: 'PList[T]', binary_op: Callable[[T, T], T], neutral: Optional[T] = None) -> T:
        if neutral is None:
            assert self.__global_size >= 1
            partial = None if self.__local_size == 0 else SList(self.__content).reduce(binary_op)
            partials = SList(_COMM.allgather(partial)).filter(lambda x: x is not None)
        else:
            # assert: (binary_op, neutral) form a monoid
            partial = SList(self.__content).reduce(binary_op, neutral)
            partials = SList(_COMM.allgather(partial))
        return partials.reduce(binary_op, neutral)

    def map_reduce(self: 'PList[T]', unary_op: Callable[[T], V],
                   binary_op: Callable[[V, V], V], neutral: Optional[V] = None) -> V:
        if neutral is None:
            assert self.__global_size >= 1
            partial = None if self.__local_size == 0 \
                else self.__content.map_reduce(unary_op, binary_op)
            partials = SList(_COMM.allgather(partial)).filter(lambda x: x is not None)
            return functools.reduce(binary_op, partials)
        # assert: (binary_op, neutral) form a monoid
        partial = self.__content.map_reduce(unary_op, binary_op, neutral)
        partials = _COMM.allgather(partial)
        return functools.reduce(binary_op, partials, neutral)

    def scanr(self: 'PList[T]', binary_op: Callable[[T, T], T]) -> 'PList[T]':
        assert self.__global_size > 0
        p_list = self.__get_shape()
        partials = self.__content.scanr(binary_op)
        last = partials[self.__local_size - 1]
        acc, _ = parimpl.scan(binary_op, last)
        if _PID != 0:
            for (index, value) in enumerate(partials):
                partials[index] = binary_op(acc, value)
        p_list.__content = partials
        return p_list

    def scanl_last(self: 'PList[T]', binary_op: Callable[[T, T], T], neutral: T) \
            -> 'Tuple[PList[T], T]':
        p_list = self.__get_shape()
        partials, last = self.__content.scanl_last(binary_op, neutral)
        acc, red = parimpl.scan(binary_op, last)
        if _PID != 0:
            for (index, value) in enumerate(partials):
                partials[index] = binary_op(acc, value)
        p_list.__content = partials
        return p_list, red

    def scanl(self: 'PList[T]', binary_op: Callable[[T, T], T], neutral: T) -> 'PList[T]':
        res, _ = self.scanl_last(binary_op, neutral)
        return res

    def distribute(self: 'PList[T]', target_distr: Distribution) -> 'PList[T]':
        assert Distribution.is_valid(target_distr, self.__global_size)
        source_distr = self.__distribution
        source_bounds = interval.bounds(source_distr)
        target_bounds = interval.bounds(target_distr)
        local_interval = source_bounds[_PID]
        bounds_to_send = target_bounds.map(lambda i: interval.intersection(i, local_interval))
        msgs = [interval.to_slice(self.__content, interval.shift(inter, -self.__start_index))
                for inter in bounds_to_send]
        slices = _COMM.alltoall(msgs)
        p_list = PList()
        p_list.__content = SList(slices).flatten()
        p_list.__local_size = target_distr[_PID]
        p_list.__global_size = self.__global_size
        p_list.__start_index = SList(target_distr).scanl(add, 0)[_PID]
        p_list.__distribution = target_distr
        return p_list

    def balance(self: 'PList[T]') -> 'PList[T]':
        return self.distribute(Distribution.balanced(self.length()))

    def gather(self: 'PList[T]', pid: int) -> 'PList[T]':
        assert pid in par.procs()
        d_list = [self.length() if i == pid else 0 for i in par.procs()]
        distr = Distribution(d_list)
        return self.distribute(distr)

    def scatter(self: 'PList[T]', pid: int) -> 'PList[T]':
        assert pid in par.procs()

        def select(index, a_list):
            if index == pid:
                return a_list
            return []

        select_distr = Distribution([size if index == pid else 0
                                     for (index, size) in enumerate(self.distribution)])
        at_pid = self.get_partition().mapi(select).flatten(select_distr)

        distr = Distribution.balanced(at_pid.length())
        return at_pid.distribute(distr)

    def scatter_range(self: 'PList[T]', rng) -> 'PList[T]':

        def select(index, value):
            if index in rng:
                return value
            return None

        def not_none(value):
            return value is not None

        selected = self.mapi(select).filter(not_none)
        distr = Distribution.balanced(selected.length())
        return selected.distribute(distr)

    @staticmethod
    def from_seq(sequence: Sequence[T]) -> 'PList[T]':
        p_list = PList()
        if _PID == 0:
            p_list.__content = SList(sequence)
            p_list.__distribution = [len(sequence) if i == 0 else 0 for i in par.procs()]
        from_root = _COMM.bcast(p_list.__distribution, 0)
        p_list.__distribution = Distribution(from_root)
        p_list.__local_size = p_list.__distribution[_PID]
        p_list.__global_size = p_list.__distribution[0]
        p_list.__start_index = SList(p_list.__distribution).scanl(add, 0)[_PID]
        return p_list

    def to_seq(self: 'PList[T]') -> 'SList[T]':
        return SList(self.get_partition().reduce(concat, []))

    def permute(self: 'PList[T]', bij: Callable[[int], int]) -> 'PList[T]':
        p_list = self.__get_shape()
        distr = Distribution(self.__distribution)
        new_indices = self.mapi(lambda i, x: distr.to_pid(bij(i), x)).get_partition().map(_group_by)
        mapping = new_indices.__content[0]
        keys = mapping.keys()
        messages = [mapping[pid] if pid in keys else [] for pid in par.procs()]
        exchanged = SList(parimpl.COMM.alltoall(messages)).flatten()
        exchanged.sort()
        p_list.__content = exchanged.map(lambda pair: pair[1])
        return p_list
