import pytest

from pyske.core.tree.ptree import *
from pyske.core.support.parallel import *
from pyske.core.tree.ltree import *

def illformed_ltree():
    seg1 = Segment([TaggedValue(13, "C")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg3])
    with pytest.raises(IllFormedError):
        PTree(lt)


def test_to_seq():
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    pt = PTree(lt)
    res = pt.to_seq()
    exp = lt if pid == 0 else None
    assert res == exp


def test_map_empty():
    pt = PTree()
    id_f = lambda x: x
    exp = PTree()
    res = pt.map(id_f, id_f)
    assert exp == res


def test_map_not_empty():
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    pt = PTree(lt)

    res = pt.map(lambda x: x + 1, lambda x: x - 1).to_seq()

    seg1_exp = Segment([TaggedValue(12, "C")])
    seg2_exp = Segment([TaggedValue(30, "N"), TaggedValue(48, "L"), TaggedValue(33, "L")])
    seg3_exp = Segment([TaggedValue(71, "N"), TaggedValue(93, "L"), TaggedValue(43, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp]) if pid == 0 else None

    assert res == exp


# -------------------------- #

def test_reduce_empty():
    pt = PTree()
    id_f = lambda x: x
    sum3 = lambda x, y, z: x + y + z
    with pytest.raises(AssertionError):
        pt.reduce(sum3, id_f, sum3, sum3, sum3)


def test_reduce():
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    pt = PTree(lt)
    id_f = lambda x: x
    sum3 = lambda x, y, z: x + y + z
    res = pt.reduce(sum3, id_f, sum3, sum3, sum3)
    exp = lt.reduce(sum3, id_f, sum3, sum3, sum3) if pid == 0 else None
    assert res == exp


# -------------------------- #

def test_uacc_empty():
    pt = PTree()
    id_f = lambda x: x
    sum3 = lambda x, y, z: x + y + z
    with pytest.raises(AssertionError):
        pt.uacc(sum3, id_f, sum3, sum3, sum3)


def test_uacc():
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    pt = PTree(lt)
    id_f = lambda x: x
    sum3 = lambda x, y, z: x + y + z
    res = pt.uacc(sum3, id_f, sum3, sum3, sum3).to_seq()

    seg1_exp = Segment([TaggedValue(13 + 31 + 47 + 32 + 72 + 92 + 42, "C")])
    seg2_exp = Segment([TaggedValue(31 + 47 + 32, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3_exp = Segment([TaggedValue(72 + 92 + 42, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp]) if pid == 0 else None
    assert exp == res

# -------------------------- #

def test_dacc():
    sum2 = lambda x, y: x + y
    c = 0
    id_f = lambda x: x
    seg1 = Segment([TaggedValue(13, "C")])
    seg2 = Segment([TaggedValue(31, "N"), TaggedValue(47, "L"), TaggedValue(32, "L")])
    seg3 = Segment([TaggedValue(72, "N"), TaggedValue(92, "L"), TaggedValue(42, "L")])
    lt = LTree([seg1, seg2, seg3])
    res = PTree(lt).dacc(sum2, sum2, c, id_f, id_f, sum2, sum2).to_seq()

    seg1_exp = Segment([TaggedValue(0, "C")])
    seg2_exp = Segment([TaggedValue(13, "N"), TaggedValue(13 + 31, "L"), TaggedValue(13 + 31, "L")])
    seg3_exp = Segment([TaggedValue(13, "N"), TaggedValue(13 + 72, "L"), TaggedValue(13 + 72, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp]) if pid == 0 else None

    assert res == exp


# -------------------------- #

def test_zip_not_same_size():
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
    seg2_exp = Segment([TaggedValue((1, 2), "N"), TaggedValue((1, 2), "L"), TaggedValue((1, 2), "L")])
    seg3_exp = Segment([TaggedValue((1, 2), "N"), TaggedValue((1, 2), "L"), TaggedValue((1, 2), "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp]) if pid == 0 else None
    assert res == exp


# -------------------------- #

def test_map2_not_same_size():
    sum2 = lambda x, y: x + y
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
    sum2 = lambda x, y: x + y
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
    res = pt1.map2(sum2, pt2).to_seq()
    seg1_exp = Segment([TaggedValue(3, "C")])
    seg2_exp = Segment([TaggedValue(3, "N"), TaggedValue(3, "L"), TaggedValue(3, "L")])
    seg3_exp = Segment([TaggedValue(3, "N"), TaggedValue(3, "L"), TaggedValue(3, "L")])
    exp = LTree([seg1_exp, seg2_exp, seg3_exp]) if pid == 0 else None
    assert res == exp