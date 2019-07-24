__all__ = ['comm', 'pid', 'nprocs', 'local_size', 'scan']

from mpi4py import MPI

comm = MPI.COMM_WORLD
pid = comm.Get_rank()
nprocs = comm.Get_size()


def local_size(i, size):
    return int(size / nprocs) + (1 if i < size % nprocs else 0)


def scan(op, x):
    xs = comm.alltoall([x for _ in range(0, nprocs)])
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
