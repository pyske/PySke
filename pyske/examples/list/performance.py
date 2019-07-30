"""
Examples of skeleton programs on lists
"""
from operator import add
import operator
import random
import math
import gc
import argparse
from pyske.core import PList as DPList, SList as DSList, par
from pyske.core.opt.list import PList as OPList, SList as OSList


def _test(test_f, data, name, preprocessing=lambda f, num: lambda: f(num), execute=lambda f: f()):
    assert ITERATIONS > 0
    par.at_root(lambda: print(f'Test: {name}'))
    skel = preprocessing(test_f, data)
    par.at_root(lambda: print("Term: ", skel))
    gc.collect()
    par.barrier()
    time: DPList = DPList.init(lambda _: par.wtime())
    output = data
    for idx in range(0, ITERATIONS):
        def printer(val):
            return lambda: print(f'  Iteration: {val}', end='\r')
        par.at_root(printer(idx))
        output = execute(skel)
    elapsed = time.map(lambda num: par.wtime() - num).map(lambda num: num / ITERATIONS)

    par.at_root(lambda: print(30 * ' ', end='\r'))
    max_elapsed = elapsed.reduce(max)
    avg_elapsed = elapsed.reduce(add) / elapsed.length()
    all_elapsed = elapsed.mapi(lambda k, num: "[" + str(k) + "]:" + str(num)).to_seq()
    par.at_root(lambda:
                print(f'Time (max):\t{max_elapsed}\n'
                      f'Time (avg):\t{avg_elapsed}\n'
                      f'Time (all):\t{all_elapsed}'))
    return output


def _f_map(num):
    return 2 * num + 1


def _f_reduce(num1, num2):
    return num1 + num2 * num2


def sqr(num):
    """
    Computes the square of its argument.
    :param num: number
    :return: number
    """
    return num*num


def smul(scalar: float, vec: DSList):
    """
    Compute the product of a scalar and a vector
    :param scalar: float
    :param vec: DSList
    :return: DSList
    """
    return vec.map(lambda num: scalar*num)


def vadd(vec1: DSList, vec2: DSList):
    """
    Computes the sum of two vectors.
    :param vec1: DSList
    :param vec2: DSList
    :return: DSList
    """
    return vec1.map2(add, vec2)


def norm(vec: DSList):
    """
    Computes the norm of the argument vector.
    :param vec: DSList
    :return: float
    """
    return math.sqrt(vec.map(sqr).reduce(add, 0))


def normalize(vec: DSList):
    """
    Normalize the input vector.
    :param vec: DSList
    :return: DSList
    """
    norm_ = norm(vec)
    return smul(1/norm_, vec)


def _opt(fct, data):
    return fct(data).opt()


def _run(term):
    return term.eval()


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--iter", help="number of iterations", type=int, default=5)
PARSER.add_argument("--size", help="size of the list to generate", type=int, default=1_000_000)
PARSER.add_argument("--seq", help="choice of the data structure", action='store_true')
PARSER.add_argument("--test", help="choice of the test", type=int, default=2)
PARSER.add_argument("-v", help="verbose mode", action='store_true')
ARGS = PARSER.parse_args()
ITERATIONS = ARGS.iter
SIZE = ARGS.size
SEQ = ARGS.seq
TST = ARGS.test
VRB = ARGS.v

if VRB:
    par.at_root(lambda:
                print("Iterations:\t", ITERATIONS,
                      "\nSize:\t", SIZE,
                      "\nSeq: \t", SEQ,
                      "\nTest:\t", TST,
                      "\nNprocs:\t", len(par.procs())))


def _test_mmr_direct(lst):
    lst1 = lst.map(_f_map)
    lst2 = lst1.map(_f_map)
    res = lst2.reduce(_f_reduce, 0)
    return res


def _test_mr_direct(lst):
    def fct(num):
        return _f_map(_f_map(num))
    lst1 = lst.map(fct)
    res = lst1.reduce(_f_reduce, 0)
    return res


def _test_mmr_run(lst):
    if SEQ:
        lst1 = OSList.raw(lst)
    else:
        lst1 = OPList.raw(lst)
    lst2 = lst1.map(_f_map)
    lst3 = lst2.map(_f_map)
    res = lst3.reduce(_f_reduce, 0)
    return res.run()


def _test_mmr_optimized(lst):
    if SEQ:
        lst1 = OSList.raw(lst)
    else:
        lst1 = OPList.raw(lst)
    lst2 = lst1.map(_f_map)
    lst3 = lst2.map(_f_map)
    res = lst3.reduce(_f_reduce, 0)
    return res


def _test_bool_direct(lst):
    return lst.map(operator.not_).reduce(operator.and_, True)


def _test_bool_optimized(lst):
    if SEQ:
        lst = OSList.raw(lst)
    else:
        lst = OPList.raw(lst)
    return _test_bool_direct(lst)


def _test_bool_mr(lst):
    return lst.map_reduce(operator.not_, operator.and_, True)


def _test1():
    if SEQ:
        input1 = DSList.init(lambda num: random.randint(0, 1000), SIZE)
    else:
        input1 = DPList.init(lambda num: random.randint(0, 1000), SIZE)
    res1 = _test(_test_mmr_direct, input1, "map/map/reduce")
    res2 = _test(_test_mmr_direct, input1, "map/reduce[hc]")
    res3 = _test(_test_mmr_run, input1, "map/map/reduce[_opt]")
    res4 = _test(_test_mmr_optimized, input1, "map/map/reduce[_opt/_run]", _opt, _run)
    assert res1 == res2 and res1 == res3 and res1 == res4


def _test2():
    if SEQ:
        input2 = DSList.init(lambda i: random.randint(0, 9) <= 4, SIZE)
    else:
        input2 = DPList.init(lambda i: random.randint(0, 9) <= 4, SIZE)
    res1 = _test(_test_bool_direct, input2, "map/reduce bool")
    res2 = _test(_test_bool_mr, input2, "map_reduce bool")
    res3 = _test(_test_bool_optimized, input2, "map/reduce bool[_opt]", _opt, _run)
    assert res1 == res3
    assert res1 == res2


DIM = 10


VZERO = DSList.init(lambda i: 0.0, DIM)


def _f_rand(_):
    return random.randint(0, 1000)


def _vrand(_):
    return DSList.init(_f_rand, DIM)


def _vnsum(lst):
    return lst.map(normalize).reduce(vadd, VZERO)


def _vavg(lst):
    scalar = 1 / lst.length()
    return smul(scalar, _vnsum(lst))


def _wrapped_vavg(lst):
    scalar = 1 / lst.length()
    lst = OSList.raw(lst) if SEQ else OPList.raw(lst)
    skel = _vnsum(lst).opt()
    res = smul(scalar, skel.eval())
    return res


def _test3():
    if SEQ:
        data = DSList.init(_vrand, SIZE)
    else:
        data = DPList.init(_vrand, SIZE)
    res1 = _test(_vavg, data, "vector average")
    res2 = _test(_wrapped_vavg, data, "vector average [_run]")
    assert res1 == res2


if __name__ == '__main__':
    if TST == 1:
        _test1()
    if TST == 2:
        _test2()
    if TST == 3:
        _test3()
