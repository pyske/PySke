import pytest
pytestmark = pytest.mark.plist

from pyske.core.list.slist import SList
from pyske.core.list.plist import PList
from pyske.core.support.parallel import nprocs, balanced_distribution
import random


msg = "hello world!"


def test_init_to_seq_empty():
    pl = PList()
    res = pl.to_seq()
    exp = []
    assert res == exp


def test_init_to_seq_non_empty():
    pl = PList.init(lambda i: msg[i], len(msg))
    res = pl.to_seq()
    exp = list(msg)
    assert res == exp


def test_map_empty():
    f = lambda x: x.upper()
    input = PList()
    res = input.map(f).to_seq()
    exp = []
    assert res == exp


def test_map_non_empty():
    f = lambda x: x.upper()
    input = PList.init(lambda i: msg[i], len(msg))
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
    op = lambda x, y: x + y
    res = pl.map_reduce(f, op)
    exp = pl.map(f).reduce(op)
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
    size = PList.from_seq([random.randint(17, 111)]).to_seq()[0]
    dst = PList.from_seq([random.randint(0, nprocs-1)]).to_seq()[0]
    input = PList.init(lambda i: i, size)
    d = [0 for _ in range(0, nprocs)]
    d[dst] = size
    res = input.distribute(d).to_seq()
    exp = SList(range(0, size))
    assert res == exp


def test_distribute_distr():
    size = PList.from_seq([random.randint(17, 111)]).to_seq()[0]
    dst = PList.from_seq([random.randint(0, nprocs - 1)]).to_seq()[0]
    input = PList.init(lambda i: i, size)
    exp = [0 for _ in range(0, nprocs)]
    exp[dst] = size
    res = input.distribute(exp).get_partition().map(len).to_seq()
    assert res == exp


def test_balance_data():
    size = PList.from_seq([random.randint(17, 111)]).to_seq()[0]
    input = PList.from_seq(list(range(0,size)))
    res = input.balance().to_seq()
    exp = SList(range(0, size))
    assert res == exp


def test_balance_distr():
    size = PList.from_seq([random.randint(17, 37)]).to_seq()[0]
    dst = PList.from_seq([random.randint(0, nprocs - 1)]).to_seq()[0]
    input = PList.init(lambda i: i, size)
    d = [0 for _ in range(0, nprocs)]
    d[dst] = size
    res = input.distribute(d).balance().get_partition().map(len).to_seq()
    exp = balanced_distribution(size)
    assert res == exp


def test_gather_data():
    size = PList.from_seq([random.randint(17, 37)]).to_seq()[0]
    dst = PList.from_seq([random.randint(0, nprocs - 1)]).to_seq()[0]
    input = PList.init(lambda i: i, size)
    res = input.gather(dst).to_seq()
    exp = input.to_seq()
    assert res == exp


def test_gather_distr():
    size = PList.from_seq([random.randint(17, 37)]).to_seq()[0]
    dst = PList.from_seq([random.randint(0, nprocs - 1)]).to_seq()[0]
    input = PList.init(lambda i: i, size)
    res = input.gather(dst).get_partition().map(len).to_seq()
    exp = [size if i == dst else 0 for i in range(0, nprocs)]
    assert res == exp