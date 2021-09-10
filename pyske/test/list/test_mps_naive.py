from pyske.core.support.maximum_subarray_problem import list_to_prefix, frdm
from pyske.examples.list.maximum_prefix_sum import *
from pyske.core.list.slist import *
from pyske.core.support.generate import random_list
import random


def test_list_to_prefix():
    list = [1, 2, 3, 4]
    prefix = list_to_prefix(list)
    res = [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4]]
    assert prefix == res


def test_mps_naive1():
    a_list = SList([1, 2, -1, 2, -1, -1, 3, -4])
    segments = list_to_prefix(a_list)
    max_sum = max(max(map(sum, segments)), 0)
    assert max_sum == 5


def test_mps_naive2():
    a_list = SList([1, 2, 1, 2, 1, 1, 3, 4])
    segments = list_to_prefix(a_list)
    max_sum = max(max(map(sum, segments)), 0)
    assert max_sum == 15


def test_mps_naive3():
    a_list = SList([-1, -2, -1, -2, -1, -1, -3, -4])
    segments = list_to_prefix(a_list)
    max_sum = max(max(map(sum, segments)), 0)
    assert max_sum == 0


def test_comparison_mps_naive_to_opti():
    a_list = random_list(frdm, random.randint(1, 15))
    segments = list_to_prefix(a_list)
    max_sum_naive = max(max(map(sum, segments)), 0)
    max_sum_opti = mps(a_list)
    assert max_sum_naive == max_sum_opti