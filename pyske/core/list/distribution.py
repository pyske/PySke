"""
distribution: lists representing PySke list distributions
"""
import functools
from operator import add

from pyske.core import interface
from pyske.core.support import parallel
from pyske.core.support.list import scan
from pyske.core.util.par import procs


class Distribution(interface.Distribution):
    """
    A class to represent the distribution of parallel linear data structure.
    """
    def is_valid(self, size: int) -> bool:
        if len(self) != parallel.NPROCS:
            return False
        for num in self:
            if num < 0:
                return False
        return size == functools.reduce(add, self, 0)

    @staticmethod
    def balanced(size: int) -> 'Distribution':
        distr = [parallel.local_size(pid, size) for pid in procs()]
        return Distribution(distr)

    def to_pid(self, index: int, value):
        indices = scan(self, add, 0)
        indices.pop(0)
        for (pid, bound) in enumerate(indices):
            if index < bound:
                return pid, (index, value)
        return parallel.NPROCS - 1, (index, value)
