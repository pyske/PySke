from pyske.core.list.plist import PList as DPList
from pyske.core.opt.list import PList as OPList
from pyske.core.list.slist import SList as DSList
from pyske.core.opt.list import SList as OSList
from pyske.core.util import par
from operator import add
import operator
import random
import math
import gc
import argparse


def test(f, data, name, preprocessing=lambda f, x: lambda: f(x), execute=lambda f: f()):
    assert(iterations > 0)
    par.at_root(lambda: print(f'Test: {name}'))
    skel = preprocessing(f, data)
    par.at_root(lambda: print("Term: ", skel))
    gc.collect()
    par.barrier()
    t: DPList = DPList.init(lambda _: par.wtime())
    output = data
    for i in range(0, iterations):
        par.at_root(lambda: print(f'  Iteration: {i}', end='\r'))
        output = execute(skel)
    elapsed = t.map(lambda x: par.wtime() - x).map(lambda x: x/iterations)

    par.at_root(lambda: print(30 * ' ', end='\r'))
    max_elapsed = elapsed.reduce(max)
    avg_elapsed = elapsed.reduce(add) / elapsed.length()
    all_elapsed = elapsed.mapi(lambda k, x: "[" + str(k) + "]:" + str(x)).to_seq()
    par.at_root(lambda:
                print(f'Time (max):\t{max_elapsed}\n'
                      f'Time (avg):\t{avg_elapsed}\n'
                      f'Time (all):\t{all_elapsed}'))
    return output


def f_map(x):
    return 2 * x + 1


def f_reduce(x, y):
    return x + y * y


def sqr(x):
    return x*x


def smul(s: float, v):
    return v.map(lambda x: s*x)


def vadd(v1, v2):
    return v1.map2(add, v2)


def norm(v):
    return math.sqrt(v.map(sqr).reduce(add, 0))


def normalize(v):
    n = norm(v)
    return smul(1/n, v)


def opt(f, data):
    return f(data).opt()


def run(t):
    return t.eval()


parser = argparse.ArgumentParser()
parser.add_argument("--iter", help="number of iterations", type=int, default=5)
parser.add_argument("--size", help="size of the list to generate", type=int, default=1_000_000)
parser.add_argument("--seq", help="choice of the data structure", action='store_true')
parser.add_argument("--test", help="choice of the test", type=int, default=2)
parser.add_argument("-v", help="verbose mode", action='store_true')
args = parser.parse_args()
iterations = args.iter
size = args.size
seq = args.seq
tst = args.test
vrb = args.v

if vrb:
    par.at_root(lambda:
                print("Iterations:\t", iterations,
                      "\nSize:\t", size,
                      "\nSeq: \t", seq,
                      "\nTest:\t", tst,
                      "\nNprocs:\t", len(par.procs())))


def test_mmr_direct(l):
    l1 = l.map(f_map)
    l2 = l1.map(f_map)
    r = l2.reduce(f_reduce, 0)
    return r


def test_mr_direct(l):
    def f(x): return f_map(f_map(x))
    l1 = l.map(f)
    r = l1.reduce(f_reduce, 0)
    return r


def test_mmr_run(l):
    if seq:
        l1 = OSList.raw(l)
    else:
        l1 = OPList.raw(l)
    l2 = l1.map(f_map)
    l3 = l2.map(f_map)
    r = l3.reduce(f_reduce, 0)
    return r.run()


def test_mmr_optimized(l):
    if seq:
        l1 = OSList.raw(l)
    else:
        l1 = OPList.raw(l)
    l2 = l1.map(f_map)
    l3 = l2.map(f_map)
    r = l3.reduce(f_reduce, 0)
    return r


def test_bool_direct(l):
    return l.map(operator.not_).reduce(operator.and_, True)


def test_bool_optimized(lst):
    if seq:
        lst = OSList.raw(lst)
    else:
        lst = OPList.raw(lst)
    return test_bool_direct(lst)


def test_bool_mr(l):
    return l.map_reduce(operator.not_, operator.and_, True)


def test1():
    if seq:
        input1 = DSList.init(lambda x: random.randint(0, 1000), size)
    else:
        input1 = DPList.init(lambda x: random.randint(0, 1000), size)
    r0 = test(test_mmr_direct, input1, "map/map/reduce")
    r1 = test(test_mmr_direct, input1, "map/reduce[hc]")
    r1_1 = test(test_mmr_run, input1, "map/map/reduce[opt]")
    r1_2 = test(test_mmr_optimized, input1, "map/map/reduce[opt/run]", opt, run)
    assert r0 == r1_1 and r0 == r1_2 and r0 == r1


def test2():
    if seq:
        input2 = DSList.init(lambda i: random.randint(0, 9) <= 4, size)
    else:
        input2 = DPList.init(lambda i: random.randint(0, 9) <= 4, size)
    r1 = test(test_bool_direct, input2, "map/reduce bool")
    r2 = test(test_bool_mr, input2, "map_reduce bool")
    r3 = test(test_bool_optimized, input2, "map/reduce bool[opt]", opt, run)
    assert r1 == r3
    assert r1 == r2


dim = 10


vzero = DSList.init(lambda i: 0.0, dim)


def f_rand(_):
    return random.randint(0, 1000)


def vrand(_):
    return DSList.init(f_rand, dim)


def vnsum(l):
    return l.map(normalize).reduce(vadd, vzero)


def vavg(l):
    d = 1 / l.length()
    return smul(d, vnsum(l))


def wrapped_vavg(lst):
    d = 1 / lst.length()
    lst = OSList.raw(lst) if seq else OPList.raw(lst)
    t = vnsum(lst).opt()
    r = smul(d, t.eval())
    return r


def test3():
    if seq:
        data = DSList.init(lambda i: vrand(i), size)
    else:
        data = DPList.init(lambda i: vrand(i), size)
    r1 = test(vavg, data, "vector average")
    r2 = test(wrapped_vavg, data, "vector average [run]")
    assert r1 == r2


if tst == 1:
    test1()
if tst == 2:
    test2()
if tst == 3:
    test3()
