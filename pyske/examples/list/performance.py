from pyske.core.list.plist import PList as DPList
from pyske.core.opt.list import PList as OPList
from pyske.core.list.slist import SList as DSList
from pyske.core.opt.list import SList as OSList
from pyske.core.support.parallel import *
from operator import add
import operator
import random
from gc import *
import sys
import argparse


def test(f, input, name, preprocessing=lambda f, x: lambda: f(x), run=lambda f: f()):
    at_root(lambda: print(f'Test: {name}'))
    skel = preprocessing(f, input)
    at_root(lambda: print("Term: ", skel))
    collect()
    barrier()
    t = DPList.init(lambda _: wtime(), nprocs)
    for i in range(0, iterations):
        at_root(lambda: print(f'  Iteration: {i}', end='\r'))
        output = run(skel)
    elapsed = t.map(lambda x: wtime() - x).map(lambda x: x/iterations)

    at_root(lambda: print(30 * ' ', end='\r'))
    max_elapsed = elapsed.reduce(max)
    avg_elapsed = elapsed.reduce(add) / nprocs
    all_elapsed = elapsed.mapi(lambda i, x: "[" + str(i) + "]:" + str(x)).to_seq()
    at_root(lambda:
            print(f'Time (max):\t{max_elapsed}\n'
                  f'Time (avg):\t{avg_elapsed}\n'
                  f'Time (all):\t{all_elapsed}'))
    return output


def incr(x):
    return x+1


def incr10(x):
    for i in range(0,100):
        x = x + 1
    return x


def opt(f, input):
    return f(input).opt()


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
    at_root(lambda:
            print("Iterations:\t",iterations,
                  "\nSize:\t", size,
                  "\nSeq: \t", seq,
                  "\nTest:\t", tst,
                  "\nNprocs:\t", nprocs))

def test_mmr_direct(l):
    l1 = l.map(incr)
    l2 = l1.map(incr)
    r = l2.reduce(add, 0)
    return r


def test_mmr_run(l):
    if seq:
        l1 = OSList.raw(l)
    else:
        l1 = OPList.raw(l)
    l2 = l1.map(incr)
    l3 = l2.map(incr)
    r = l3.reduce(add, 0)
    return r.run()


def test_mmr_optimized(l):
    if seq:
        l1 = OSList.raw(l)
    else:
        l1 = OPList.raw(l)
    l2 = l1.map(incr)
    l3 = l2.map(incr)
    r = l3.reduce(add, 0)
    return r


def test_bool_direct(l):
    return l.map(operator.not_).reduce(operator.and_, True)


def test_bool_optimized(l):
    if seq:
        l = OSList.raw(l)
    else:
        l = OPList.raw(l)
    return test_bool_direct(l)


def test_bool_mr(l):
    return l.map_reduce(operator.not_, operator.and_, True)


def test1():
    if seq:
        input1 = DSList.init(lambda x: x, size)
    else:
        input1 = DPList.init(lambda x: x, size)
    r0   = test(test_mmr_direct, input1, "map/map/reduce")
    r1_1 = test(test_mmr_run, input1, "map/map/reduce[opt]")
    r1_2 = test(test_mmr_optimized, input1, "map/map/reduce[opt/run]", opt, run)
    assert r0 == r1_1 and r0 == r1_2


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

if tst == 1: test1()
if tst == 2: test2()
