def __pos(inter, i):
    if inter is None:
        return None
    else:
        return inter[i]

def interval(l,u):
    if l <= u:
        return (l,u)
    else:
        return None

def lower(inter):
    return __pos(inter, 0)


def upper(inter):
    return __pos(inter, 1)


def is_valid(inter):
    return (inter is None) or ((type(inter) is tuple) and (lower(inter) <= upper(inter)))


def union(inter1, inter2):
    assert (is_valid(inter1))
    assert (is_valid(inter2))
    if inter1 is None:
        return inter2
    if inter2 is None:
        return inter1
    return (min(lower(inter1), lower(inter2)),
            max(upper(inter1), upper(inter2)))


def intersection(inter1, inter2):
    assert (is_valid(inter1))
    assert (is_valid(inter2))
    if (inter1 is None or inter2 is None or upper(inter1) < lower(inter2) or upper(inter2) < lower(inter1)):
        return None
    else:
        return (max(lower(inter1), lower(inter2)),
                min(upper(inter1), upper(inter2)))

def shift(inter, offset):
    if inter is None:
        return None
    else:
        return (lower(inter)+offset, upper(inter)+offset)

def slice(list, inter):
    is_valid(inter)
    if inter is None:
        return []
    else:
        return list[lower(inter):upper(inter)+1]