"""
PTree test module
"""
import pytest

from pyske.core.tree.ltree import IllFormedError, LTree
from pyske.core.tree.ptree import Segment, TaggedValue, PTree
from pyske.core.support.parallel import PID
from pyske.core.util import fun


def illformed_ltree():
    # pylint: disable=missing-docstring
    seg1 = Segment([TaggedValue(13, "C")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg3])
    with pytest.raises(IllFormedError):
        PTree(lt)


def test_to_seq():
    # pylint: disable=missing-docstring
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    pt = PTree(lt)
    res = pt.to_seq()
    exp = lt if PID == 0 else None
    assert res == exp


def test_map_empty():
    # pylint: disable=missing-docstring
    pt = PTree()
    exp = PTree()
    res = pt.map(fun.idt, fun.idt)
    assert exp == res


def test_map_not_empty():
    # pylint: disable=missing-docstring
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    pt = PTree(lt)

    res = pt.map(lambda x: x + 1, lambda x: x - 1).to_seq()

    seg1_exp = Segment([TaggedValue(12, "C")])
    seg2_exp = Segment([TaggedValue(30, "N"), TaggedValue(48, "L"), TaggedValue(33, "L")])
    seg3_exp = Segment([TaggedValue(71, "N"), TaggedValue(93, "L"), TaggedValue(43, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp]) if PID == 0 else None

    assert res == exp


# -------------------------- #

def test_reduce_empty():
    # pylint: disable=missing-docstring
    pt = PTree()
    with pytest.raises(AssertionError):
        pt.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add)


def test_reduce():
    # pylint: disable=missing-docstring
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    pt = PTree(lt)
    res = pt.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add)
    exp = lt.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add) if PID == 0 else None
    assert res == exp


# -------------------------- #

def test_uacc_empty():
    # pylint: disable=missing-docstring
    pt = PTree()
    with pytest.raises(AssertionError):
        pt.uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)


def test_uacc():
    # pylint: disable=missing-docstring
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    pt = PTree(lt)
    res = pt.uacc(fun.add, fun.idt, fun.add, fun.add, fun.add).to_seq()

    seg1_exp = Segment([TaggedValue(13 + 31 + 47 + 32 + 72 + 92 + 42, "C")])
    seg2_exp = Segment([TaggedValue(31 + 47 + 32, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3_exp = Segment([TaggedValue(72 + 92 + 42, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp]) if PID == 0 else None
    assert exp == res


# -------------------------- #

def test_dacc():
    # pylint: disable=missing-docstring
    c = 0
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    res = PTree(lt).dacc(fun.add, fun.add, c, fun.idt, fun.idt, fun.add, fun.add).to_seq()

    seg1_exp = Segment([TaggedValue(0, "C")])
    seg2_exp = Segment([TaggedValue(13, "N"), TaggedValue(13 + 31, "L"), TaggedValue(13 + 31, "L")])
    seg3_exp = Segment([TaggedValue(13, "N"), TaggedValue(13 + 72, "L"), TaggedValue(13 + 72, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp]) if PID == 0 else None

    assert res == exp


# -------------------------- #

def test_zip_not_same_size():
    # pylint: disable=missing-docstring
    seg11 = Segment([TaggedValue(13, "C")])
    seg21 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg31 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt1 = LTree([seg11, seg21, seg31])
    seg22 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    lt2 = LTree([seg22])
    pt1 = PTree(lt1)
    pt2 = PTree(lt2)
    with pytest.raises(AssertionError):
        pt1.zip(pt2)


def test_zip():
    # pylint: disable=missing-docstring
    seg11 = Segment([TaggedValue(1, "C")])
    seg21 = Segment([TaggedValue(1, "N"), TaggedValue(1, "L"), TaggedValue(1, "L")])
    seg31 = Segment([TaggedValue(1, "N"), TaggedValue(1, "L"), TaggedValue(1, "L")])
    lt1 = LTree([seg11, seg21, seg31])
    seg12 = Segment([TaggedValue(2, "C")])
    seg22 = Segment([TaggedValue(2, "N"), TaggedValue(2, "L"), TaggedValue(2, "L")])
    seg32 = Segment([TaggedValue(2, "N"), TaggedValue(2, "L"), TaggedValue(2, "L")])
    lt2 = LTree([seg12, seg22, seg32])
    pt1 = PTree(lt1)
    pt2 = PTree(lt2)
    res = pt1.zip(pt2).to_seq()
    seg1_exp = Segment([TaggedValue((1, 2), "C")])
    seg2_exp = Segment([TaggedValue((1, 2), "N"),
                        TaggedValue((1, 2), "L"),
                        TaggedValue((1, 2), "L")])
    seg3_exp = Segment([TaggedValue((1, 2), "N"),
                        TaggedValue((1, 2), "L"),
                        TaggedValue((1, 2), "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp]) if PID == 0 else None
    assert res == exp


# -------------------------- #

def test_map2_not_same_size():
    # pylint: disable=missing-docstring
    seg11 = Segment([TaggedValue(13, "C")])
    seg21 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg31 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt1 = LTree([seg11, seg21, seg31])
    seg22 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    lt2 = LTree([seg22])
    pt1 = PTree(lt1)
    pt2 = PTree(lt2)
    with pytest.raises(AssertionError):
        pt1.zip(pt2)


def test_map2():
    # pylint: disable=missing-docstring
    seg11 = Segment([TaggedValue(1, "C")])
    seg21 = Segment([TaggedValue(1, "N"), TaggedValue(1, "L"), TaggedValue(1, "L")])
    seg31 = Segment([TaggedValue(1, "N"), TaggedValue(1, "L"), TaggedValue(1, "L")])
    lt1 = LTree([seg11, seg21, seg31])
    seg12 = Segment([TaggedValue(2, "C")])
    seg22 = Segment([TaggedValue(2, "N"), TaggedValue(2, "L"), TaggedValue(2, "L")])
    seg32 = Segment([TaggedValue(2, "N"), TaggedValue(2, "L"), TaggedValue(2, "L")])
    lt2 = LTree([seg12, seg22, seg32])
    pt1 = PTree(lt1)
    pt2 = PTree(lt2)
    res = pt1.map2(fun.add, pt2).to_seq()
    seg1_exp = Segment([TaggedValue(3, "C")])
    seg2_exp = Segment([TaggedValue(3, "N"), TaggedValue(3, "L"), TaggedValue(3, "L")])
    seg3_exp = Segment([TaggedValue(3, "N"), TaggedValue(3, "L"), TaggedValue(3, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp]) if PID == 0 else None
    assert res == exp
