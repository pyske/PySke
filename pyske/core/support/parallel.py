"""
Internal module providing basic parallel functions
"""
__all__ = ['COMM', 'PID', 'NPROCS', 'local_size', 'scan']

from typing import Callable, TypeVar, Tuple
from mpi4py import MPI

T = TypeVar('T')    # pylint: disable=invalid-name

COMM = MPI.COMM_WORLD  # pylint: disable=c-extension-no-member
PID = COMM.Get_rank()
NPROCS = COMM.Get_size()


def local_size(pid: int, size: int) -> int:
    """
    :param pid: a process identifier (0 <= pid < NPROCS)
    :param size: a positive integer
    :return: the number of elements the processor should contain for a linear
    data structure of the given size.
    """
    assert 0 <= pid < NPROCS
    assert size >= 0
    return int(size / NPROCS) + (1 if pid < size % NPROCS else 0)


def scan(binary_op: Callable[[T, T], T], value: T) -> Tuple[T, T]:
    """
    :param binary_op: a binary operation
    :param value: each processor possess such a value
    :return: prefix sum
    """
    values = COMM.alltoall([value for _ in range(0, NPROCS)])
    pre = values[0]
    for i in range(1, PID):
        pre = binary_op(pre, values[i])
    res = values[PID]
    for i in range(PID + 1, NPROCS):
        res = binary_op(res, values[i])
    if PID != 0:
        return pre, binary_op(pre, res)
    return pre, res
