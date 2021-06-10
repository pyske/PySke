import random
from pyske.core.support.maximum_subarray_problem import list_to_segment, frdm, list_2d_to_segment
from pyske.core.list.slist import *
from pyske.examples.list.maximum_segment_sum import *
from pyske.core.support.generate import random_list


def test_list_to_segment():
    list = [1, 2, 3, 4]
    segs = list_to_segment(list)
    res = [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [2], [2, 3], [2, 3, 4], [3], [3, 4], [4]]
    assert segs == res


def test_list_2d_to_segment():
    list = [[-1, 2], [6, 1]]
    segs = list_2d_to_segment(list)
    res = [[-1, 2, 6, 1], [-1, 6], [-1, 2], [-1], [2, 1], [2], [6, 1], [6], [1]]
    assert segs == res


def test_max_segments_sum_naive():
    a_list = SList([-5, 2, 6, -4, 5, -6, -4, 3])
    segments = list_to_segment(a_list)
    max_sum = max(max(map(sum, segments)), 0)
    assert max_sum == 9


def test_max_segments_sum_naive2():
    a_list = SList([5, 2, 6, 4, 5, 6, 4, 3])
    segments = list_to_segment(a_list)
    max_sum = max(max(map(sum, segments)), 0)
    assert max_sum == 35


def test_max_segments_sum_naive3():
    a_list = SList([-5, -2, -6, -4, -5, -6, -4, -3])
    segments = list_to_segment(a_list)
    max_sum = max(max(map(sum, segments)), 0)
    assert max_sum == 0


def test_comparison_mss_naive_to_opti():
    a_list = random_list(frdm, random.randint(1, 15))
    segments = list_to_segment(a_list)
    max_sum_naive = max(max(map(sum, segments)), 0)
    max_sum_opti = maximum_segment_sum(a_list)
    assert max_sum_naive == max_sum_opti


def test_max_segment_problem_2d_list():
    list = SList([[-1, 2], [6, 1], [-4, 3]])
    segs = list_2d_to_segment(list)
    res = max(max(map(sum, segs)), 0)
    assert res == 8


def test_max_segment_problem_2d_list2():
    list = SList([[1, 2], [6, 1], [4, 3]])
    segs = list_2d_to_segment(list)
    res = max(max(map(sum, segs)), 0)
    assert res == 17


def test_max_segment_problem_2d_list3():
    list = SList([[-1, -2], [-6, -1], [-4, -2]])
    segs = list_2d_to_segment(list)
    res = max(max(map(sum, segs)), 0)
    assert res == 0