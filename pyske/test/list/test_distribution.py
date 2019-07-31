"""
Tests for parallel util functions and class
"""

__all__ = []

import random
from pyske.core.support import parallel
from pyske.core.list.distribution import Distribution


def test_distribution_is_valid():
    # pylint: disable=missing-docstring
    tmp = parallel.NPROCS
    parallel.NPROCS = 4
    distr = [4, 12, 27, 18]
    size = sum(distr)
    res = Distribution(distr).is_valid(size)
    parallel.NPROCS = tmp
    assert res


def test_distribution_is_not_valid():
    # pylint: disable=missing-docstring
    distr = [4, 12, 27, 18]
    size = sum(distr)
    res = Distribution(distr).is_valid(size - 1)
    assert not res


def test_distribution_balanced_valid():
    # pylint: disable=missing-docstring
    size = random.randint(0, 100)
    distr = Distribution.balanced(size)
    res = distr.is_valid(size)
    assert res


def test_distribution_balanced_not_valid():
    # pylint: disable=missing-docstring
    size = random.randint(10, 100)
    distr = Distribution.balanced(size)
    res = distr.is_valid(size-1)
    assert not res


def test_distribution_pid_of_index_0():
    # pylint: disable=missing-docstring
    value = random.randint(0, 100)
    distr = Distribution([4, 12, 27, 18])
    res = distr.to_pid(3, value)
    exp = 0, (3, value)
    assert exp == res


def test_distribution_pid_of_index_1():
    # pylint: disable=missing-docstring
    value = random.randint(0, 100)
    distr = Distribution([4, 12, 27, 18])
    res = distr.to_pid(9, value)
    exp = 1, (9, value)
    assert exp == res


def test_distribution_pid_of_index_2():
    # pylint: disable=missing-docstring
    value = random.randint(0, 100)
    distr = Distribution([4, 12, 27, 18])
    res = distr.to_pid(20, value)
    exp = 2, (20, value)
    assert exp == res


def test_distribution_pid_of_index_3():
    # pylint: disable=missing-docstring
    value = random.randint(0, 100)
    distr = Distribution([4, 12, 27, 18])
    res = distr.to_pid(43, value)
    exp = 3, (43, value)
    assert exp == res


def test_distribution_pid_of_index_with_empty_1():
    # pylint: disable=missing-docstring
    value = random.randint(0, 100)
    distr = Distribution([0, 10, 0, 20])
    res = distr.to_pid(9, value)
    exp = 1, (9, value)
    assert exp == res


def test_distribution_pid_of_index_with_empty_3():
    # pylint: disable=missing-docstring
    value = random.randint(0, 100)
    distr = Distribution([0, 10, 0, 20])
    res = distr.to_pid(10, value)
    exp = 3, (10, value)
    assert exp == res
