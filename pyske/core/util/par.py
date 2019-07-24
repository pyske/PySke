__all__ = ['procs', 'wtime', 'barrier', 'Distribution', 'at_root']

from pyske.core.support import parallel
from operator import add
from mpi4py import MPI
import functools
import random


def randpid():
    return random.randint(0, parallel.nprocs - 1)


def procs():
    return range(0, parallel.nprocs)


def wtime():
    return MPI.Wtime()


def barrier():
    parallel.comm.barrier()


class Distribution(list):

    def is_valid(self, size):
        if len(self) != parallel.nprocs:
            return False
        for s in self:
            if s < 0:
                return False
        return size == functools.reduce(add, self, 0)

    @staticmethod
    def balanced(size):
        d = [parallel.local_size(i, size) for i in procs()]
        return Distribution(d)


def at_root(f):
    if parallel.pid == 0:
        return f()
    else:
        return None
