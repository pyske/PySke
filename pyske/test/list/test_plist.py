import pytest

pytestmark = pytest.mark.plist

from pyske.core.list.slist import SList
from pyske.core.list.plist import PList
from pyske.core.support.parallel import nprocs, balanced_distribution
import random

msg = "Hello World!"


def id(x): return x


def alphabet(i):
    return chr(65 + (i % 26))


def is_even(x):
    return x % 2 ==0


def randint(min, max):
    return PList.from_seq([random.randint(min, max)]).to_seq()[0]


def randpid():
    return randint(0, nprocs - 1)


def generate_plist(f, n=0):
    choice = randint(n, 2)
    size = randint(0, 111)
    if choice == 0:
        return PList()
    elif choice == 1:
        return PList.init(f, size)
    else:
        return PList.from_seq([f(i) for i in range(0, size)])


def generate_int_plist(n=0):
    return generate_plist(id, n)


def generate_str_plist(n=0):
    return generate_plist(alphabet, n)


def upper(s):
    return s.upper()


def incr(x):
    return x + 1


def get_distribution(pl: PList):
    return pl.get_partition().map(len).to_seq()


def test_init_to_seq_empty():
    pl = PList()
    res = pl.to_seq()
    exp = []
    assert res == exp


def test_init_to_seq_non_empty():
    pl = PList.init(alphabet, 17)
    res = pl.to_seq()
    exp = [alphabet(i) for i in range(0, 17)]
    assert res == exp


def test_map_empty():
    input = PList()
    res = input.map(upper).to_seq()
    exp = []
    assert res == exp


def test_map_non_empty():
    input = generate_int_plist()
    res = input.map(incr).to_seq()
    exp = input.to_seq().map(incr)
    assert res == exp


def test_map_from_seq():
    f = lambda x: x.upper()
    input = PList.from_seq(msg)
    input.invariant()
    res = input.map(f).to_seq()
    exp = list(f(msg))
    assert res == exp


def test_mapi_empty():
    f = lambda i, x: f'{i}:{x.upper()}'
    input = PList()
    res = input.mapi(f).to_seq()
    exp = []
    assert res == exp


# -------------------------- #

def test_reduce_nil():
    e = 0
    sl = SList()
    pl = PList.from_seq(sl)
    f = lambda x, y: x + y
    res = pl.reduce(f, e)
    exp = e
    assert res == exp


def test_reduce_cons():
    sl = SList([1, 2, 3, 4])
    pl = PList.from_seq(sl)
    f = lambda x, y: x + y
    res = pl.reduce(f)
    exp = 10
    assert res == exp


def test_reduce_sum_empty():
    e = 0
    sl = SList()
    pl = PList.from_seq(sl)
    f = lambda x, y: x + y
    exp = e
    res = pl.reduce(f, e)
    assert res == exp


def test_reduce_sum_non_empty():
    sl = SList([1, 2, 3, 4, 5, 6])
    pl = PList.from_seq(sl)
    f = lambda x, y: x + y
    exp = 21
    res = pl.reduce(f, 0)
    assert res == exp


# -------------------------- #

def test_map_reduce_nil():
    e = 0
    sl = SList()
    pl = PList.from_seq(sl)
    f = lambda x: x + 1
    op = lambda x, y: x + y
    res = pl.map_reduce(f, op, e)
    exp = e
    assert res == exp


def test_map_reduce_cons():
    sl = SList([1, 2, 3, 4])
    pl = PList.from_seq(sl)
    f = lambda x: x + 1
    op = lambda x, y: x + 1
    exp = pl.map(f)
    exp = exp.reduce(op)
    res = pl.map_reduce(f, op)
    assert res == exp


# -------------------------- #

def test_mapi_non_empty():
    f = lambda i, x: f'{i}:{x.upper()}'
    input = PList.init(lambda i: msg[i], len(msg))
    res = input.mapi(f).to_seq()
    exp = SList(msg).mapi(f)
    assert res == exp


def test_scanr_non_empty():
    f = lambda x, y: x + y
    size = 23
    input = PList.init(lambda i: i, size)
    res = input.scanr(f).to_seq()
    exp = SList(range(0, size)).scanr(f)
    assert res == exp


def test_scanl_empty():
    f = lambda x, y: x + y
    size = 0
    input = PList.init(lambda i: i, size)
    res = input.scanl(f, 0).to_seq()
    exp = SList(range(0, size)).scanl(f, 0)
    assert res == exp


def test_scanl_non_empty():
    f = lambda x, y: x + y
    size = 23
    input = PList.init(lambda i: i, size)
    res = input.scanl(f, 0).to_seq()
    exp = SList(range(0, size)).scanl(f, 0)
    assert res == exp


def test_scanl_last_empty():
    f = lambda x, y: x + y
    size = 0
    input = PList.init(lambda i: i, size)
    res_pl, res_scalar = input.scanl_last(f, 0)
    res = (res_pl.to_seq(), res_scalar)
    exp = SList(range(0, size)).scanl_last(f, 0)
    assert res == exp


def test_scanl_last_non_empty():
    f = lambda x, y: x + y
    size = 23
    input = PList.init(lambda i: i, size)
    res_pl, res_scalar = input.scanl_last(f, 0)
    res = (res_pl.to_seq(), res_scalar)
    exp = SList(range(0, size)).scanl_last(f, 0)
    assert res == exp


def test_distribute_data():
    dst = randpid()
    input = generate_int_plist()
    size = input.length()
    d = [0 for _ in range(0, nprocs)]
    d[dst] = size
    res = input.distribute(d).to_seq()
    exp = SList(range(0, size))
    assert res == exp


def test_distribute_distr():
    input = generate_str_plist()
    size = input.length()
    dst = randpid()
    exp = [0 for _ in range(0, nprocs)]
    exp[dst] = size
    res = get_distribution(input.distribute(exp))
    assert res == exp


def test_balance_data():
    input = generate_int_plist()
    size = input.length()
    res = input.balance().to_seq()
    exp = SList(range(0, size))
    assert res == exp


def test_balance_distr():
    input = generate_str_plist()
    size = input.length()
    dst = randpid()
    d = [0 for _ in range(0, nprocs)]
    d[dst] = size
    res = get_distribution(input.distribute(d).balance())
    exp = balanced_distribution(size)
    assert res == exp


def test_gather_data():
    input = generate_str_plist()
    dst = randpid()
    res = input.gather(dst).to_seq()
    exp = input.to_seq()
    assert res == exp


def test_gather_distr():
    input = generate_str_plist()
    size = input.length()
    dst = randpid()
    res = get_distribution(input.gather(dst))
    exp = [size if i == dst else 0 for i in range(0, nprocs)]
    assert res == exp


def test_scatter_data():
    input = generate_str_plist()
    src = randpid()
    res = input.scatter(src).to_seq()
    exp = input.get_partition().to_seq()[src]
    assert res == exp


def test_scatter_distr():
    input = generate_str_plist()
    src = randpid()
    distr = get_distribution(input)
    res = get_distribution(input.scatter(src))
    exp = balanced_distribution(distr[src])
    assert res == exp


def test_scatter_range_data():
    input = generate_str_plist()
    n = input.length()
    if 0 < n:
        min = randint(0, n - 1)
        max = randint(min, n - 1)
    else:
        min = 0
        max = 0
    res = input.scatter_range(range(min, max)).to_seq()
    exp = input.to_seq()[min:max]
    assert res == exp


def test_scatter_range_distr():
    input = generate_str_plist()
    n = input.length()
    if 0 < n:
        min = randint(0, n - 1)
        max = randint(min, n - 1)
    else:
        min = 0
        max = 0
    res = get_distribution(input.scatter_range(range(min, max)))
    exp = balanced_distribution(max - min)
    assert res == exp


def test_filter():
    input = generate_int_plist().map(lambda i: random.randint(0, 100))
    res = input.filter(is_even).to_seq()
    exp = input.to_seq().filter(is_even)
    assert exp == res
    for x in res:
        assert is_even(x)
