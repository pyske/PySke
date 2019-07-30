"""
Operations on intervals.
"""
from operator import add
from pyske.core.list.slist import SList


def __pos(inter, idx):
    if inter is None:
        return None
    return inter[idx]


def interval(lower_, upper_):
    """Build an interval."""
    if lower_ <= upper_:
        return lower_, upper_
    return None


def lower(inter):
    """Return the lower bound of an interval."""
    return __pos(inter, 0)


def upper(inter):
    """Return the upper bound of an interval."""
    return __pos(inter, 1)


def is_valid(inter):
    """Check the validity of an interval."""
    return (inter is None) or (isinstance(inter, tuple) and (lower(inter) <= upper(inter)))


def union(inter1, inter2):
    """Union two intervals."""
    assert is_valid(inter1)
    assert is_valid(inter2)
    if inter1 is None:
        return inter2
    if inter2 is None:
        return inter1
    return (min(lower(inter1), lower(inter2)),
            max(upper(inter1), upper(inter2)))


def intersection(inter1, inter2):
    """Intersect two intervals."""
    assert is_valid(inter1)
    assert is_valid(inter2)
    if (inter1 is None or inter2 is None or
            upper(inter1) < lower(inter2) or
            upper(inter2) < lower(inter1)):
        return None
    return (max(lower(inter1), lower(inter2)),
            min(upper(inter1), upper(inter2)))


def shift(inter, offset):
    """Shift an interval by an offset."""
    if inter is None:
        return None
    return lower(inter) + offset, upper(inter) + offset


def to_slice(lst, inter):
    """Slice a list using an interval."""
    assert is_valid(inter)
    if inter is None:
        return []
    return lst[lower(inter):upper(inter) + 1]


def _firsts(distr):
    return SList(distr).scanl(add, 0)


def _lasts(distr):
    return SList(distr).scan(add, 0).tail().map(lambda x: x - 1)


def bounds(distr):
    """Bounds in a distribution"""
    return _firsts(distr).map2(interval, _lasts(distr))
