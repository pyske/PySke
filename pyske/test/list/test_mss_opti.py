from pyske.examples.list.maximum_segment_sum import *
from pyske.core.list.slist import *


def test_max_segments_sum_opti():
    a_list = SList([-5, 2, 6, -4, 5, -6, -4, 3])
    max_sum = maximum_segment_sum(a_list)
    assert max_sum == 9


def test_max_segments_sum_opti2():
    a_list = SList([5, 2, 6, 4, 5, 6, 4, 3])
    max_sum = maximum_segment_sum(a_list)
    assert max_sum == 35


def test_max_segments_sum_opti3():
    a_list = SList([-5, -2, -6, -4, -5, -6, -4, -3])
    max_sum = maximum_segment_sum(a_list)
    assert max_sum == 0


def test_max_segments_sum_opti4():
    a_list = SList([])
    max_sum = maximum_segment_sum(a_list)
    assert max_sum == 0