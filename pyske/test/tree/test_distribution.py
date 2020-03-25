from pyske.core.tree.distribution import *

from pyske.core.support import parallel


def test_balanced_segs():
    # init nb proc
    tmp = parallel.NPROCS
    parallel.NPROCS = 3

    sizes = [5, 3, 3, 5, 5, 1, 1, 3]
    dist = Distribution.balanced_segs(sizes)
    res_dist, res_global = dist.distribution, dist.global_index
    exp_dist = [3, 3, 2]
    exp_global = [(0, 5), (5, 3), (8, 3), (0, 5), (5, 5), (10, 1), (0, 1), (1, 3)]

    # reset nb proc
    parallel.NPROCS = tmp

    assert res_dist == exp_dist
    assert res_global == exp_global


def test_balanced_tree():
    # init nb proc
    tmp = parallel.NPROCS
    parallel.NPROCS = 3

    sizes = [5, 3, 3, 5, 5, 1, 1, 3]
    dist = Distribution.balanced_tree(sizes)
    res_dist, res_global = dist.distribution, dist.global_index
    exp_dist = [2, 2, 4]
    exp_global = [(0, 5), (5, 3), (0, 3), (3, 5), (0, 5), (5, 1), (6, 1), (7, 3)]

    # reset nb proc
    parallel.NPROCS = tmp

    assert res_dist == exp_dist
    assert res_global == exp_global