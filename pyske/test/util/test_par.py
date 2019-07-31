"""
Tests for parallel util functions and class
"""

__all__ = []

from pyske.core.support import parallel
from pyske.core.util import par


def test_rand_pid():
    # pylint: disable=missing-docstring
    val = par.randpid()
    assert val in range(0, parallel.NPROCS)
