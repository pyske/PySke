"""
Non-skeletal Parallel Functions
"""

__all__ = ['procs', 'wtime', 'barrier', 'at_root']


from typing import Callable
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


def at_root(execute: Callable[[], None]) -> None:
    """
    Executes the given function only at processor 0.

    :param execute: the function to execute.
    """
    if parallel.PID == 0:
        execute()
