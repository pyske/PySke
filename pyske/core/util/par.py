"""
Non-skeletal Parallel Functions
"""

__all__ = ['procs', 'wtime', 'barrier', 'Distribution', 'at_root']


from typing import Callable
from operator import add
import functools
import random
from mpi4py import MPI
from pyske.core.list.slist import SList
from pyske.core.support import parallel
from pyske.core.interface.linear import IDistribution


def randpid() -> int:
    """
    If called by different processors, the result may be different on each calling processor.

    :return: a random processor identifier.
    """
    return random.randint(0, parallel.NPROCS - 1)


def procs() -> range:
    """
    :return: the list of available processor identifiers.
    """
    return range(0, parallel.NPROCS)


def wtime() -> float:
    """
    :return:  the current time as a floating point number.
    """
    return MPI.Wtime()  # pylint: disable=c-extension-no-member


def barrier() -> None:
    """
    Synchronizes all the processors of the parallel machine.

    :return: None
    """
    parallel.COMM.barrier()


class Distribution(IDistribution):
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

    def to_pid(self, idx: int, value):
        indices = SList(self).scan(add, 0)
        # size = indices[len(indices) - 1]
        # assert self.is_valid(size)
        indices.pop(0)
        for (pid, bound) in enumerate(indices):
            if idx < bound:
                return pid, (idx, value)
        return parallel.NPROCS - 1, (idx, value)


def at_root(execute: Callable[[], None]) -> None:
    """
    Executes the given function only at processor 0.

    :param execute: the function to execute.
    """
    if parallel.PID == 0:
        execute()
