"""
A module of parallel lists and associated skeletons
"""
from operator import add
import functools
from typing import TypeVar, Callable, Generic
from pyske.core.support import parallel as parimpl, interval
from pyske.core.util import par
from pyske.core.list.slist import SList

__all__ = ['PList']

_PID: int = parimpl.pid
_NPROCS: int = parimpl.nprocs
_COMM = parimpl.comm

T = TypeVar('T')  # pylint: disable=invalid-name
R = TypeVar("R")  # pylint: disable=invalid-name


class PList(Generic[T]):
    # pylint: disable=too-many-public-methods
    # pylint: disable=protected-access
    """Distributed lists"""

    def __init__(self):
        self.__content: SList[T] = SList([])
        self.__global_size = 0
        self.__local_size = 0
        self.__start_index = 0
        self.__distribution = [0 for _ in range(0, _NPROCS)]

    def __get_shape(self):
        plst = PList()
        plst.__local_size = self.__local_size
        plst.__global_size = self.__global_size
        plst.__distribution = self.__distribution
        plst.__start_index = self.__start_index
        return plst

    def __str__(self):
        return "pid[" + str(_PID) + "]:\n" + \
               "  global_size: " + str(self.__global_size) + "\n" + \
               "  local_size: " + str(self.__local_size) + "\n" + \
               "  start_index: " + str(self.__start_index) + "\n" + \
               "  distribution: " + str(self.__distribution) + "\n" + \
               "  content: " + str(self.__content) + "\n"

    def invariant(self):
        assert isinstance(self.__content, SList)
        prefix = SList(self.__distribution).scan(add, 0)
        assert len(self.__content) == self.__local_size
        assert self.__distribution[_PID] == self.__local_size
        assert self.__start_index == prefix[_PID]
        assert prefix[_NPROCS] == self.__global_size

    def length(self) -> int:
        return self.__global_size

    @staticmethod
    def init(value_at: Callable[[int], T], size: int = _NPROCS):
        assert size >= 0
        plst: PList[T] = PList()
        plst.__global_size = size
        plst.__local_size = parimpl.local_size(_PID, size)
        plst.__distribution = [parimpl.local_size(i, size) for i in range(0, _NPROCS)]
        plst.__start_index = SList(plst.__distribution).scanl(lambda x, y: x + y, 0)[_PID]
        plst.__content = SList([value_at(i) for i in
                                range(plst.__start_index, plst.__start_index + plst.__local_size)])
        plst.__distribution = [parimpl.local_size(i, size) for i in range(0, _NPROCS)]
        return plst

    def map(self, unop: Callable[[T], R]):
        """
        :param unop: a unary function.
        :return: a new parallel list obtained by applying the unary operation to all
        the elements of self.
        """
        plst: PList[R] = self.__get_shape()
        plst.__content = self.__content.map(unop)
        return plst

    def mapi(self, fct):
        plst = self.__get_shape()
        plst.__content = self.__content.mapi(lambda i, x: fct(i + self.__start_index, x))
        return plst

    def map2(self, fct, plst):
        assert self.__distribution == plst.__distribution
        res = self.__get_shape()
        res.__content = self.__content.map2(fct, plst.__content)
        return res

    def map2i(self, fct, plst):
        assert self.__distribution == plst.__distribution
        res = self.__get_shape()
        res.__content = self.__content.map2i(lambda i, x, y:
                                             fct(i + self.__start_index, x, y), plst.__content)
        return res

    def zip(self, plst):
        return self.map2(lambda x, y: (x, y), plst)

    def filter(self, predicate):
        return self.get_partition().map(lambda l: l.filter(predicate)).flatten()

    def get_partition(self):
        plst = PList()
        plst.__content = SList([self.__content])
        plst.__global_size = _NPROCS
        plst.__local_size = 1
        plst.__start_index = _PID
        plst.__distribution = [1 for _ in par.procs()]
        return plst

    def flatten(self):
        plst = PList()
        plst.__content = self.__content.flatten()
        plst.__local_size = len(plst.__content)
        plst.__distribution = _COMM.allgather(plst.__local_size)
        plst.__start_index = SList(plst.__distribution).scanl(add, 0)[_PID]
        plst.__global_size = SList(plst.__distribution).reduce(add)
        return plst

    def reduce(self, operation, neutral=None):
        if neutral is None:
            assert self.__global_size >= 1
            partial = None if self.__local_size == 0 else SList(self.__content).reduce(operation)
            partials = SList(_COMM.allgather(partial)).filter(lambda x: x is not None)
        else:
            # assert: (operation, neutral) form a monoid
            partial = SList(self.__content).reduce(operation, neutral)
            partials = SList(_COMM.allgather(partial))
        return partials.reduce(operation, neutral)

    def map_reduce(self, fct, operation, neutral=None):
        if neutral is None:
            assert self.__global_size >= 1
            partial = None if self.__local_size == 0 else self.__content.map_reduce(fct, operation)
            partials = SList(_COMM.allgather(partial)).filter(lambda x: x is not None)
            return functools.reduce(operation, partials)
        # assert: (operation, neutral) form a monoid
        partial = self.__content.map_reduce(fct, operation, neutral)
        partials = _COMM.allgather(partial)
        return functools.reduce(operation, partials, neutral)

    def scanr(self, operation):
        assert self.__global_size > 0
        plst = self.__get_shape()
        partials = self.__content.scanr(operation)
        last = partials[self.__local_size - 1]
        acc, _ = parimpl.scan(operation, last)
        if _PID != 0:
            for (idx, value) in enumerate(partials):
                partials[idx] = operation(acc, value)
        plst.__content = partials
        return plst

    def scanl(self, operation, neutral):
        plst = self.__get_shape()
        partials, last = self.__content.scanl_last(operation, neutral)
        acc, _ = parimpl.scan(operation, last)
        if _PID != 0:
            for (idx, value) in enumerate(partials):
                partials[idx] = operation(acc, value)
        plst.__content = partials
        return plst

    def scanl_last(self, operation, neutral):
        plst = self.__get_shape()
        partials, last = self.__content.scanl_last(operation, neutral)
        acc, red = parimpl.scan(operation, last)
        if _PID != 0:
            for (idx, value) in enumerate(partials):
                partials[idx] = operation(acc, value)
        plst.__content = partials
        return plst, red

    def distribute(self, target_distr):
        assert par.Distribution.is_valid(target_distr, self.__global_size)
        source_distr = self.__distribution
        source_bounds = interval.bounds(source_distr)
        target_bounds = interval.bounds(target_distr)
        local_interval = source_bounds[_PID]
        bounds_to_send = target_bounds.map(lambda i: interval.intersection(i, local_interval))
        msgs = [interval.to_slice(self.__content, interval.shift(inter, -self.__start_index))
                for inter in bounds_to_send]
        slices = _COMM.alltoall(msgs)
        plst = PList()
        plst.__content = SList(slices).flatten()
        plst.__local_size = target_distr[_PID]
        plst.__global_size = self.__global_size
        plst.__start_index = SList(target_distr).scanl(add, 0)[_PID]
        plst.__distribution = target_distr
        return plst

    def balance(self):
        return self.distribute(par.Distribution.balanced(self.__global_size))

    def gather(self, pid):
        assert pid in par.procs()
        distr = [self.length() if i == pid else 0 for i in par.procs()]
        return self.distribute(distr)

    def gather_at_root(self):
        return self.gather(0)

    def scatter(self, pid):
        assert pid in par.procs()

        def select(idx, lst):
            if idx == pid:
                return lst
            return []

        at_pid = self.get_partition().mapi(select).flatten()
        return at_pid.distribute(par.Distribution.balanced(at_pid.length()))

    def scatter_from_root(self):
        return self.scatter(0)

    def scatter_range(self, rng):
        def select(idx, value):
            if idx in rng:
                return value
            return None

        def not_none(value):
            return value is not None

        selected = self.mapi(select).filter(not_none)
        return selected.distribute(par.Distribution.balanced(selected.length()))

    @staticmethod
    def from_seq(lst):
        plst = PList()
        if _PID == 0:
            plst.__content = SList(lst)
            plst.__distribution = [len(lst) if i == 0 else 0 for i in par.procs()]
        from_root = _COMM.bcast(plst.__distribution, 0)
        plst.__distribution = from_root
        plst.__local_size = plst.__distribution[_PID]
        plst.__global_size = plst.__distribution[0]
        plst.__start_index = SList(plst.__distribution).scanl(add, 0)[_PID]
        return plst

    def to_seq(self):
        return SList(self.get_partition().reduce(lambda x, y: x + y, []))
