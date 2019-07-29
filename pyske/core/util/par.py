"""
Non-skeletal Parallel Functions
"""
__all__ = ['procs', 'wtime', 'barrier', 'Distribution', 'at_root']


from typing import Callable
from operator import add
import functools
import random
from mpi4py import MPI
from pyske.core.support import parallel


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


class Distribution(list):
    """
    A class to represent the distribution of parallel linear data structure.
    """
    def is_valid(self, size: int) -> bool:
        """
        Checks if the current distribution really represent the distribution
        a of linear structure of the given size. Each element of the distribution
        should be positive, its length should be equal to the number of
        available processors, and the sum of all its elements should be
        equal to the given size.

        :param size: should be >= 0
        :return: bool
        """
        if len(self) != parallel.NPROCS:
            return False
        for num in self:
            if num < 0:
                return False
        return size == functools.reduce(add, self, 0)

    @staticmethod
    def balanced(size: int) -> 'Distribution':
        """
        :param size: should be >= 0
        :return: Returns a balanced distribution, i.e. a distribution
        such that for any two elements, their differ by at most 1.
        The sum of all the elements is size.
        """
        distr = [parallel.local_size(pid, size) for pid in procs()]
        return Distribution(distr)


def at_root(execute: Callable[[], None]) -> None:
    """
    Executes the given function only at processor 0.

    :param execute: the function to execute.
    """
    if parallel.PID == 0:
        execute()
