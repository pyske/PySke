"""
Tests for parallel lists and associated skeletons
"""
__all__ = []
import operator
import random

import pytest

from pyske.core.list.plist import PList
from pyske.core.list.slist import SList
from pyske.core.util import fun
from pyske.core.util import par

# pylint: disable=invalid-name
pytestmark = pytest.mark.plist

MSG = "Hello World!"


def alphabet(num):
    """
    Returns a capital letter from a number.
    :param num: int
    :return:
    """
    return chr(65 + (num % 26))


def is_even(num):
    """
    Tests is its argument is even.
    :param num: int
    :return: bool
    """
    return num % 2 == 0


def randint(min_, max_):
    """
    Returns the same random number on all the processors.
    :param min_: int
    :param max_: int
    :return: int
    """
    return PList.from_seq([random.randint(min_, max_)]).to_seq()[0]


def rand_min_max(size):
    """
    Returns a pair of random numbers between 0 and ``size-1``, such
    that the first component is smaller or equal to the second component.
    :param size: int
    :return: int, int
    """
    assert size >= 0
    if size > 0:
        min_val = randint(0, size - 1)
        max_val = randint(min_val, size - 1)
        return min_val, max_val
    return 0, 0


def upper_case(string):
    """
    Returns its argument in upper case.
    :param string: str
    :return: str
    """
    return string.upper()


def pos_upper(num, string):
    """
    Returns a string containing its first argument, and its second argument in upper case.

    :param num: int
    :param string: str
    :return: str
    """
    return f'{num}:{string.upper()}'


def generate_plist(function, start=0):
    """
    Generates a parallel list of random size between 1 and 111, or an empty list,
    using ``function`` to initialize the elements of the list. If ``start`` is 1,
    a non-empty parallel list is generated.

    :param function: callable
    :param start: int (0 or 1)
    :return: PList
    """
    choice = randint(start, 2)
    size = randint(1, 111)
    if choice == 0:
        return PList()
    if choice == 1:
        return PList.init(function, size)
    return PList.from_seq([function(i) for i in range(0, size)])


def generate_int_plist(start=0):
    """
    Generates the parallel list ``[0, ..., n ]`` where ``n``is a random number between 1 and 111.
    If ``start`` is 1, a non-empty parallel list is generated.

    :param start: int (0 or 1)
    :return: PList
    """
    return generate_plist(fun.idt, start)


def generate_str_plist(start=0):
    """
    Generates the parallel list ``[alphabet(0),`` ... ``, alphabet(n) ]``
    where ``n``is a random number between 1 and 111.
    If ``start`` is 1, a non-empty parallel list is generated.

    :param start: int (0 or 1)
    :return: PList
    """
    return generate_plist(alphabet, start)


def get_distribution(plst: PList):
    """
    Returns the distribution (as a sequential list) of its argument.

    :param plst: PList
    :return: list
    """
    return plst.get_partition().map(len).to_seq()


def test_init_to_seq_empty():
    # pylint: disable=missing-docstring
    plst = PList()
    res = plst.to_seq()
    exp = []
    assert res == exp


def test_init_to_seq_non_empty():
    # pylint: disable=missing-docstring
    plst = PList.init(alphabet, 17)
    res = plst.to_seq()
    exp = [alphabet(i) for i in range(0, 17)]
    assert res == exp


def test_map_empty():
    # pylint: disable=missing-docstring
    data = PList()
    res = data.map(upper_case).to_seq()
    exp = []
    assert res == exp


def test_map_non_empty():
    # pylint: disable=missing-docstring
    data = generate_int_plist()
    res = data.map(fun.incr).to_seq()
    exp = data.to_seq().map(fun.incr)
    assert res == exp


def test_map_from_seq():
    # pylint: disable=missing-docstring
    data = PList.from_seq(MSG)
    data.invariant()
    res = data.map(upper_case).to_seq()
    exp = list(upper_case(MSG))
    assert res == exp


def test_mapi_empty():
    # pylint: disable=missing-docstring
    data = PList()
    res = data.mapi(pos_upper).to_seq()
    exp = []
    assert res == exp


# -------------------------- #

def test_reduce_nil():
    # pylint: disable=missing-docstring
    neutral = 0
    slst = SList()
    plst = PList.from_seq(slst)
    res = plst.reduce(operator.add, neutral)
    exp = neutral
    assert res == exp


def test_reduce_cons():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3, 4])
    plst = PList.from_seq(slst)
    res = plst.reduce(operator.add)
    exp = 10
    assert res == exp


def test_reduce_sum_empty():
    # pylint: disable=missing-docstring
    neutral = 0
    slst = SList()
    plst = PList.from_seq(slst)
    exp = neutral
    res = plst.reduce(operator.add, neutral)
    assert res == exp


def test_reduce_sum_non_empty():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3, 4, 5, 6])
    plst = PList.from_seq(slst)
    exp = 21
    res = plst.reduce(operator.add, 0)
    assert res == exp


# -------------------------- #

def test_map_reduce_nil():
    # pylint: disable=missing-docstring
    neutral = 0
    slst = SList()
    plst = PList.from_seq(slst)
    res = plst.map_reduce(fun.incr, operator.add, neutral)
    exp = neutral
    assert res == exp


def test_map_reduce_cons():
    # pylint: disable=missing-docstring
    slst = SList([1, 2, 3, 4])
    plst = PList.from_seq(slst)
    exp = plst.map(fun.incr)
    exp = exp.reduce(operator.add)
    res = plst.map_reduce(fun.incr, operator.add)
    assert res == exp


# -------------------------- #

def test_mapi_non_empty():
    # pylint: disable=missing-docstring
    data = PList.init(lambda i: MSG[i], len(MSG))
    res = data.mapi(pos_upper).to_seq()
    exp = SList(MSG).mapi(pos_upper)
    assert res == exp


def test_scanr_non_empty():
    # pylint: disable=missing-docstring
    size = 23
    data = PList.init(fun.idt, size)
    res = data.scanr(operator.add).to_seq()
    exp = SList(range(0, size)).scanr(operator.add)
    assert res == exp


def test_scanl_empty():
    # pylint: disable=missing-docstring
    size = 0
    data = PList.init(fun.idt, size)
    res = data.scanl(operator.add, 0).to_seq()
    exp = SList(range(0, size)).scanl(operator.add, 0)
    assert res == exp


def test_scanl_non_empty():
    # pylint: disable=missing-docstring
    size = 23
    data = PList.init(fun.idt, size)
    res = data.scanl(operator.add, 0).to_seq()
    exp = SList(range(0, size)).scanl(operator.add, 0)
    assert res == exp


def test_scanl_last_empty():
    # pylint: disable=missing-docstring
    size = 0
    data = PList.init(fun.idt, size)
    res_pl, res_scalar = data.scanl_last(operator.add, 0)
    res = (res_pl.to_seq(), res_scalar)
    exp = SList(range(0, size)).scanl_last(operator.add, 0)
    assert res == exp


def test_scanl_last_non_empty():
    # pylint: disable=missing-docstring
    size = 23
    data = PList.init(fun.idt, size)
    res_pl, res_scalar = data.scanl_last(operator.add, 0)
    res = (res_pl.to_seq(), res_scalar)
    exp = SList(range(0, size)).scanl_last(operator.add, 0)
    assert res == exp


def test_distribute_data():
    # pylint: disable=missing-docstring
    dst = par.randpid()
    data = generate_int_plist()
    size = data.length()
    distr = [0 for _ in par.procs()]
    distr[dst] = size
    res = data.distribute(distr).to_seq()
    exp = SList(range(0, size))
    assert res == exp


def test_distribute_distr():
    # pylint: disable=missing-docstring
    data = generate_str_plist()
    size = data.length()
    dst = par.randpid()
    exp = [0 for _ in par.procs()]
    exp[dst] = size
    res = get_distribution(data.distribute(exp))
    assert res == exp


def test_balance_data():
    # pylint: disable=missing-docstring
    data = generate_int_plist()
    size = data.length()
    res = data.balance().to_seq()
    exp = SList(range(0, size))
    assert res == exp


def test_balance_distr():
    # pylint: disable=missing-docstring
    data = generate_str_plist()
    size = data.length()
    dst = par.randpid()
    distr = [0 for _ in par.procs()]
    distr[dst] = size
    res = get_distribution(data.distribute(distr).balance())
    exp = par.Distribution.balanced(size)
    assert res == exp


def test_gather_data():
    # pylint: disable=missing-docstring
    data = generate_str_plist()
    dst = par.randpid()
    res = data.gather(dst).to_seq()
    exp = data.to_seq()
    assert res == exp


def test_gather_distr():
    # pylint: disable=missing-docstring
    data = generate_str_plist()
    size = data.length()
    dst = par.randpid()
    res = get_distribution(data.gather(dst))
    exp = [size if i == dst else 0 for i in par.procs()]
    assert res == exp


def test_scatter_data():
    # pylint: disable=missing-docstring
    data = generate_str_plist()
    src = par.randpid()
    res = data.scatter(src).to_seq()
    exp = data.get_partition().to_seq()[src]
    assert res == exp


def test_scatter_distr():
    # pylint: disable=missing-docstring
    data = generate_str_plist()
    src = par.randpid()
    distr = get_distribution(data)
    res = get_distribution(data.scatter(src))
    exp = par.Distribution.balanced(distr[src])
    assert res == exp


def test_scatter_range_data():
    # pylint: disable=missing-docstring
    data = generate_str_plist()
    min_, max_ = rand_min_max(data.length())
    res = data.scatter_range(range(min_, max_)).to_seq()
    exp = data.to_seq()[min_:max_]
    assert res == exp


def test_scatter_range_distr():
    # pylint: disable=missing-docstring
    data = generate_str_plist()
    min_, max_ = rand_min_max(data.length())
    res = get_distribution(data.scatter_range(range(min_, max_)))
    exp = par.Distribution.balanced(max_ - min_)
    assert res == exp


def test_filter():
    # pylint: disable=missing-docstring
    data = generate_int_plist().map(lambda i: random.randint(0, 100))
    res = data.filter(is_even).to_seq()
    exp = data.to_seq().filter(is_even)
    assert exp == res
    for value in res:
        assert is_even(value)
