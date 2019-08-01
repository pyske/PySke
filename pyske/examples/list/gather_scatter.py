"""
Experiments on scatter and gather
"""

import functools
from operator import concat, add
from mpi4py import MPI
from pyske.core.support.parallel import local_size
from pyske.core.support.list import scan
from pyske.core import PList
from pyske.examples.list import performance


def _pyske_gather(input_list: PList):
    return input_list.gather(0)


def _pyske_scatter(input_list: PList):
    return input_list.scatter(0)


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


def __performance():
    performance.ITERATIONS = 30
    input_list = PList.init(str, 500_000)
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
    performance.test_timing(_mpi_scatter, mpi_input_scatter, "MPI Scatter")


if __name__ == "__main__":
    # comm = MPI.COMM_WORLD
    # pid = comm.Get_rank()
    # res = comm.scatter([[1, 2],[3, 4]])
    # print(f'[{pid}]:\t{res}')
    __performance()
