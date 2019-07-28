"""
Non-skeletal Parallel Functions
"""
__all__ = ['procs', 'wtime', 'barrier', 'Distribution', 'at_root']

from operator import add
import functools
import random
from mpi4py import MPI
from pyske.core.support import parallel


def randpid():
    """
    Returns a random processor identifier.

    :return: number
    """
    return random.randint(0, parallel.nprocs - 1)


def procs():
    """
    Returns the list of available processor identifiers.

    :return: list
    """
    return range(0, parallel.nprocs)


def wtime():
    """
    Returns the current time as a floating point number.

    :return: float
    """
    return MPI.Wtime()


def barrier():
    """
    Synchronizes all the processors of the parallel machine.

    :return: None
    """
    parallel.comm.barrier()


class Distribution(list):
    """
    A class to represent the distribution of parallel linear data structure.
    """
    def is_valid(self, size):
        """
        Checks if the current distribution really represent the distribution
        a of linear structure of the given size. Each element of the distribution
        should be positive, its length should be equal to the number of
        available processors, and the sum of all its elements should be
        equal to the given size.

        :param size: int
        :return: bool
        """
        if len(self) != parallel.nprocs:
            return False
        for num in self:
            if num < 0:
                return False
        return size == functools.reduce(add, self, 0)

    @staticmethod
    def balanced(size):
        """
        Returns a balanced distribution, i.e. a distribution
        such that for any two elements, their differ by at most 1.
        The sum of all the elements is ``size``.

        :param size: int
        :return: Distribution
        """
        distr = [parallel.local_size(pid, size) for pid in procs()]
        return Distribution(distr)


def at_root(execute):
    """
    Executes the given function only at processor 0.
    ``execute`` is not supposed to take any argument.

    :param execute: callable
    """
    if parallel.pid == 0:
        execute()