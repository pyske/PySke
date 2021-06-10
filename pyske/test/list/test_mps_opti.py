from pyske.examples.list.maximum_prefix_sum import *
from pyske.core.list.slist import *


def test_mps_opti():
    a_list = SList([1, 2, -1, 2, -1, -1, 3, -4])
    best_sum = mps(a_list)
    assert best_sum == 5


def test_mps_opti2():
    a_list = SList([1, 2, 1, 2, 1, 1, 3, 4])
    best_sum = mps(a_list)
    assert best_sum == 15


def test_mps_opti3():
    a_list = SList([-1, -2, -1, -2, -1, -1, -3, -4])
    best_sum = mps(a_list)
    assert best_sum == 0


def test_mps_opti4():
    a_list = SList([])
    best_sum = mps(a_list)
    assert best_sum == 0