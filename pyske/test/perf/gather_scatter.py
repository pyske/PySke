"""
Experiments on scatter and gather
"""

import functools
from operator import concat, add
from mpi4py import MPI
from pyske.core.support.parallel import local_size
from pyske.core.support.list import scan
from pyske.core import PList, par, Distribution
from pyske.test.perf import performance


def _parse_command_line():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", help="size of the list to generate", type=int, default=100_000)
    parser.add_argument("--iter", help="number of iterations", type=int, default=30)
    args = parser.parse_args()
    return max(0, args.size), max(0, args.iter)


def _pyske_gather(input_list: PList):
    return input_list.gather(0)


def _pyske_scatter(input_list: PList):
    return input_list.scatter(0)


def _pyske_bcast(input_list: PList):
    size = input_list.distribution[0]
    nprocs = len(par.procs())
    return input_list\
        .get_partition()\
        .mapi(lambda pid, a_list: list(map(lambda _: a_list, par.procs())) if pid == 0 else []) \
        .flatten(Distribution([nprocs if pid == 0 else 0 for pid in par.procs()])) \
        .distribute(Distribution(map(lambda _: 1, par.procs())))\
        .flatten(Distribution(map(lambda _: size, par.procs())))


def _mpi_gather(input_list):
    comm = MPI.COMM_WORLD  # pylint: disable=c-extension-no-member
    gathered = comm.gather(input_list, 0)
    if gathered is None:
        gathered = []
    return functools.reduce(concat, gathered, [])


def _mpi_scatter(input_list):
    comm = MPI.COMM_WORLD  # pylint: disable=c-extension-no-member
    nprocs = comm.Get_size()
    input_size = len(input_list)
    local_sizes = list(map(lambda dst: local_size(dst, input_size), range(0, nprocs)))
    accumulated_sizes = scan(local_sizes, add, 0)
    bounds = zip(accumulated_sizes[0:nprocs], accumulated_sizes[1:])
    to_scatter = map(lambda bound: input_list[bound[0]:bound[1]], bounds)
    scattered = comm.scatter(to_scatter, 0)
    return scattered


def _mpi_scatter_alltoall(input_list):
    comm = MPI.COMM_WORLD  # pylint: disable=c-extension-no-member
    nprocs = comm.Get_size()
    rank = comm.Get_rank()
    to_scatter = list(map(lambda _: [], range(0, nprocs)))
    if rank == 0:
        input_size = len(input_list)
        local_sizes = list(map(lambda dst: local_size(dst, input_size), range(0, nprocs)))
        accumulated_sizes = scan(local_sizes, add, 0)
        bounds = zip(accumulated_sizes[0:nprocs], accumulated_sizes[1:])
        to_scatter = map(lambda bound: input_list[bound[0]:bound[1]], bounds)
    scattered = comm.alltoall(to_scatter)
    return scattered


def _mpi_bcast(input_list):
    comm = MPI.COMM_WORLD   # pylint: disable=c-extension-no-member
    broadcast = comm.bcast(input_list, 0)
    return broadcast


def __performance():
    size, num_iter = _parse_command_line()
    performance.ITERATIONS = num_iter
    input_list = PList.init(str, size)
    mpi_input_list = None

    def mpi_set(value):
        nonlocal mpi_input_list
        mpi_input_list = value

    input_list.get_partition().map(mpi_set)
    pyske_input_scatter = \
        performance.test_timing(_pyske_gather, input_list, "PySke Gather")
    mpi_input_scatter = \
        performance.test_timing(_mpi_gather, mpi_input_list, "MPI Gather")
    performance.test_timing(_pyske_scatter, pyske_input_scatter, "PySke Scatter")
    performance.test_timing(_mpi_scatter, mpi_input_scatter, "MPI Scatter (with alltoall)")
    performance.test_timing(_mpi_scatter, mpi_input_scatter, "MPI Scatter (with scatter)")
    performance.test_timing(_pyske_bcast, input_list, "PySke Bcast")
    performance.test_timing(_mpi_bcast, mpi_input_list, "MPI Bcast")


if __name__ == "__main__":
    #print(_pyske_bcast(PList.from_seq([1, 2, 3, 4, 5])))
    __performance()
