from pyske.core.list.slist import SList
from pyske.core.support.interval import *
from operator import add
from mpi4py import MPI

comm = MPI.COMM_WORLD
pid = comm.Get_rank()
nprocs = comm.Get_size()


def wtime():
    return MPI.Wtime()


def local_size_pid(i, size):
    return int(size / nprocs) + (1 if i < size % nprocs else 0)


def local_size(size):
    return local_size_pid(pid, size)


def procs():
    return range(0, nprocs)

def barrier():
    comm.barrier()

def balanced_distribution(size):
    return [local_size_pid(i, size) for i in procs()]


def is_distribution(distr, size):
    if len(distr) != nprocs:
        return False
    for s in distr:
        if s < 0: return False
    return size == SList(distr).reduce(add)


def firsts(distr):
    return SList(distr).scanl(add, 0)


def lasts(distr):
    return SList(distr).scan(add, 0).tail().map(lambda x: x - 1)


def bounds(distr):
    return firsts(distr).map2(interval, lasts(distr))


def at_root(f):
    if pid == 0:
        return f()
    else:
        return None


def scan(op, x):
    xs = comm.alltoall([x for _ in procs()])
    pre = xs[0]
    for i in range(1, pid):
        pre = op(pre, xs[i])
    res = xs[pid]
    for i in range(pid + 1, nprocs):
        res = op(res, xs[i])
    if pid != 0:
        return pre, op(pre, res)
    else:
        return pre, res