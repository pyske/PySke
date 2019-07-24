import pytest
from pyske.core.list.slist import SList
from pyske.core.list.plist import PList
from pyske.core.util import par
from pyske.core.util import fun
import random
import operator

pytestmark = pytest.mark.plist

msg = "Hello World!"


def alphabet(i):
    return chr(65 + (i % 26))


def is_even(x):
    return x % 2 == 0


def randint(min_, max_):
    return PList.from_seq([random.randint(min_, max_)]).to_seq()[0]


def upper_case(x):
    return x.upper()


def pos_upper(i, x):
    return f'{i}:{x.upper()}'


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
    return generate_plist(fun.idt, n)


def generate_str_plist(n=0):
    return generate_plist(alphabet, n)


def upper(s):
    return s.upper()


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
    data = PList()
    res = data.map(upper).to_seq()
    exp = []
    assert res == exp


def test_map_non_empty():
    data = generate_int_plist()
    res = data.map(fun.incr).to_seq()
    exp = data.to_seq().map(fun.incr)
    assert res == exp


def test_map_from_seq():
    data = PList.from_seq(msg)
    data.invariant()
    res = data.map(upper_case).to_seq()
    exp = list(upper_case(msg))
    assert res == exp


def test_mapi_empty():
    data = PList()
    res = data.mapi(pos_upper).to_seq()
    exp = []
    assert res == exp


# -------------------------- #

def test_reduce_nil():
    e = 0
    sl = SList()
    pl = PList.from_seq(sl)
    res = pl.reduce(operator.add, e)
    exp = e
    assert res == exp


def test_reduce_cons():
    sl = SList([1, 2, 3, 4])
    pl = PList.from_seq(sl)
    res = pl.reduce(operator.add)
    exp = 10
    assert res == exp


def test_reduce_sum_empty():
    e = 0
    sl = SList()
    pl = PList.from_seq(sl)
    exp = e
    res = pl.reduce(operator.add, e)
    assert res == exp


def test_reduce_sum_non_empty():
    sl = SList([1, 2, 3, 4, 5, 6])
    pl = PList.from_seq(sl)
    exp = 21
    res = pl.reduce(operator.add, 0)
    assert res == exp


# -------------------------- #

def test_map_reduce_nil():
    e = 0
    sl = SList()
    pl = PList.from_seq(sl)
    res = pl.map_reduce(fun.incr, operator.add, e)
    exp = e
    assert res == exp


def test_map_reduce_cons():
    sl = SList([1, 2, 3, 4])
    pl = PList.from_seq(sl)
    exp = pl.map(fun.incr)
    exp = exp.reduce(operator.add)
    res = pl.map_reduce(fun.incr, operator.add)
    assert res == exp


# -------------------------- #

def test_mapi_non_empty():
    data = PList.init(lambda i: msg[i], len(msg))
    res = data.mapi(pos_upper).to_seq()
    exp = SList(msg).mapi(pos_upper)
    assert res == exp


def test_scanr_non_empty():
    size = 23
    data = PList.init(fun.idt, size)
    res = data.scanr(operator.add).to_seq()
    exp = SList(range(0, size)).scanr(operator.add)
    assert res == exp


def test_scanl_empty():
    size = 0
    data = PList.init(fun.idt, size)
    res = data.scanl(operator.add, 0).to_seq()
    exp = SList(range(0, size)).scanl(operator.add, 0)
    assert res == exp


def test_scanl_non_empty():
    size = 23
    data = PList.init(fun.idt, size)
    res = data.scanl(operator.add, 0).to_seq()
    exp = SList(range(0, size)).scanl(operator.add, 0)
    assert res == exp


def test_scanl_last_empty():
    size = 0
    data = PList.init(fun.idt, size)
    res_pl, res_scalar = data.scanl_last(operator.add, 0)
    res = (res_pl.to_seq(), res_scalar)
    exp = SList(range(0, size)).scanl_last(operator.add, 0)
    assert res == exp


def test_scanl_last_non_empty():
    size = 23
    data = PList.init(fun.idt, size)
    res_pl, res_scalar = data.scanl_last(operator.add, 0)
    res = (res_pl.to_seq(), res_scalar)
    exp = SList(range(0, size)).scanl_last(operator.add, 0)
    assert res == exp


def test_distribute_data():
    dst = par.randpid()
    data = generate_int_plist()
    size = data.length()
    d = [0 for _ in par.procs()]
    d[dst] = size
    res = data.distribute(d).to_seq()
    exp = SList(range(0, size))
    assert res == exp


def test_distribute_distr():
    data = generate_str_plist()
    size = data.length()
    dst = par.randpid()
    exp = [0 for _ in par.procs()]
    exp[dst] = size
    res = get_distribution(data.distribute(exp))
    assert res == exp


def test_balance_data():
    data = generate_int_plist()
    size = data.length()
    res = data.balance().to_seq()
    exp = SList(range(0, size))
    assert res == exp


def test_balance_distr():
    data = generate_str_plist()
    size = data.length()
    dst = par.randpid()
    d = [0 for _ in par.procs()]
    d[dst] = size
    res = get_distribution(data.distribute(d).balance())
    exp = par.Distribution.balanced(size)
    assert res == exp


def test_gather_data():
    data = generate_str_plist()
    dst = par.randpid()
    res = data.gather(dst).to_seq()
    exp = data.to_seq()
    assert res == exp


def test_gather_distr():
    data = generate_str_plist()
    size = data.length()
    dst = par.randpid()
    res = get_distribution(data.gather(dst))
    exp = [size if i == dst else 0 for i in par.procs()]
    assert res == exp


def test_scatter_data():
    data = generate_str_plist()
    src = par.randpid()
    res = data.scatter(src).to_seq()
    exp = data.get_partition().to_seq()[src]
    assert res == exp


def test_scatter_distr():
    data = generate_str_plist()
    src = par.randpid()
    distr = get_distribution(data)
    res = get_distribution(data.scatter(src))
    exp = par.Distribution.balanced(distr[src])
    assert res == exp


def test_scatter_range_data():
    data = generate_str_plist()
    n = data.length()
    if 0 < n:
        min_ = randint(0, n - 1)
        max_ = randint(min_, n - 1)
    else:
        min_ = 0
        max_ = 0
    res = data.scatter_range(range(min_, max_)).to_seq()
    exp = data.to_seq()[min_:max_]
    assert res == exp


def test_scatter_range_distr():
    data = generate_str_plist()
    n = data.length()
    if 0 < n:
        min_ = randint(0, n - 1)
        max_ = randint(min_, n - 1)
    else:
        min_ = 0
        max_ = 0
    res = get_distribution(data.scatter_range(range(min_, max_)))
    exp = par.Distribution.balanced(max_ - min_)
    assert res == exp


def test_filter():
    data = generate_int_plist().map(lambda i: random.randint(0, 100))
    res = data.filter(is_even).to_seq()
    exp = data.to_seq().filter(is_even)
    assert exp == res
    for x in res:
        assert is_even(x)
