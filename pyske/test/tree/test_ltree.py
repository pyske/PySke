import pytest
import operator
from pyske.core.util import fun
from pyske.core.support.errors import IllFormedError
from pyske.core.tree.ltree import LTree, Segment, TaggedValue


def test_map_empty():
    lt = LTree()
    with pytest.raises(AssertionError):
        lt.map(fun.idt, fun.idt)


def test_map_not_empty():
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    res = lt.map(fun.incr, fun.decr)
    seg1_exp = Segment([TaggedValue(12, "C")])
    seg2_exp = Segment([TaggedValue(30, "N"), TaggedValue(48, "L"), TaggedValue(33, "L")])
    seg3_exp = Segment([TaggedValue(71, "N"), TaggedValue(93, "L"), TaggedValue(43, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp])
    assert res == exp


# -------------------------- #

def test_reduce_empty():
    lt = LTree()
    with pytest.raises(AssertionError):
        lt.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add)


def test_reduce_illformed():
    seg1 = Segment([TaggedValue(13, "C")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg3])
    with pytest.raises(IllFormedError):
        lt.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add)


def test_reduce():
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    res = lt.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add)
    exp = 13 + 31 + 47 + 32 + 72 + 92 + 42
    assert res == exp


# -------------------------- #

def test_uacc_empty():
    lt = LTree()
    with pytest.raises(AssertionError):
        lt.uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)


def test_uacc_illformed():
    seg1 = Segment([TaggedValue(13, "C")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg3])
    with pytest.raises(IllFormedError):
        lt.uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)


def test_uacc():
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    res = lt.uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)

    seg1_exp = Segment([TaggedValue(13 + 31 + 47 + 32 + 72 + 92 + 42, "C")])
    seg2_exp = Segment([TaggedValue(31 + 47 + 32, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3_exp = Segment([TaggedValue(72 + 92 + 42, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp])

    assert exp == res


# -------------------------- #

def test_dacc_empty():
    c = 0
    lt = LTree()
    with pytest.raises(AssertionError):
        lt.dacc(operator.add, operator.add, c, fun.idt, fun.idt, operator.add, operator.add)


def test_dacc():
    c = 0
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    res = lt.dacc(operator.add, operator.add, c, fun.idt, fun.idt, operator.add, operator.add)
    seg1_exp = Segment([TaggedValue(0, "C")])
    seg2_exp = Segment([TaggedValue(13, "N"), TaggedValue(13 + 31, "L"), TaggedValue(13 + 31, "L")])
    seg3_exp = Segment([TaggedValue(13, "N"), TaggedValue(13 + 72, "L"), TaggedValue(13 + 72, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp])
    assert res == exp


# -------------------------- #

def test_zip_not_same_size():
    seg11 = Segment([TaggedValue(13, "C")])
    seg21 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg31 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt1 = LTree([seg11, seg21, seg31])
    seg12 = Segment([TaggedValue(13, "C")])
    seg22 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    lt2 = LTree([seg12, seg22])
    with pytest.raises(AssertionError):
        lt1.zip(lt2)


def test_zip():
    seg11 = Segment([TaggedValue(1, "C")])
    seg21 = Segment([TaggedValue(1, "N"), TaggedValue(1, "L"), TaggedValue(1, "L")])
    seg31 = Segment([TaggedValue(1, "N"), TaggedValue(1, "L"), TaggedValue(1, "L")])
    lt1 = LTree([seg11, seg21, seg31])
    seg12 = Segment([TaggedValue(2, "C")])
    seg22 = Segment([TaggedValue(2, "N"), TaggedValue(2, "L"), TaggedValue(2, "L")])
    seg32 = Segment([TaggedValue(2, "N"), TaggedValue(2, "L"), TaggedValue(2, "L")])
    lt2 = LTree([seg12, seg22, seg32])
    res = lt1.zip(lt2)
    seg1_exp = Segment([TaggedValue((1, 2), "C")])
    seg2_exp = Segment([TaggedValue((1, 2), "N"), TaggedValue((1, 2), "L"), TaggedValue((1, 2), "L")])
    seg3_exp = Segment([TaggedValue((1, 2), "N"), TaggedValue((1, 2), "L"), TaggedValue((1, 2), "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp])
    assert res == exp


# -------------------------- #

def test_map2_not_same_size():
    seg11 = Segment([TaggedValue(13, "C")])
    seg21 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg31 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt1 = LTree([seg11, seg21, seg31])
    seg12 = Segment([TaggedValue(13, "C")])
    seg22 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    lt2 = LTree([seg12, seg22])
    with pytest.raises(AssertionError):
        lt1.map2(operator.add, lt2)


def test_map2():
    seg11 = Segment([TaggedValue(1, "C")])
    seg21 = Segment([TaggedValue(1, "N"), TaggedValue(1, "L"), TaggedValue(1, "L")])
    seg31 = Segment([TaggedValue(1, "N"), TaggedValue(1, "L"), TaggedValue(1, "L")])
    lt1 = LTree([seg11, seg21, seg31])
    seg12 = Segment([TaggedValue(2, "C")])
    seg22 = Segment([TaggedValue(2, "N"), TaggedValue(2, "L"), TaggedValue(2, "L")])
    seg32 = Segment([TaggedValue(2, "N"), TaggedValue(2, "L"), TaggedValue(2, "L")])
    lt2 = LTree([seg12, seg22, seg32])
    res = lt1.map2(operator.add, lt2)
    seg1_exp = Segment([TaggedValue(3, "C")])
    seg2_exp = Segment([TaggedValue(3, "N"), TaggedValue(3, "L"), TaggedValue(3, "L")])
    seg3_exp = Segment([TaggedValue(3, "N"), TaggedValue(3, "L"), TaggedValue(3, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp])
    assert res == exp
