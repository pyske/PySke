"""
Functions on trees
"""
from operator import add
from pyske.core.util import fun

__all__ = ['size', 'size_by_node', 'sum_values', 'prefix', 'ancestors', 'depth', 'lca', 'l_ancestors', 'lca2']


def _incr(num1, num2):
    return num1 + num2 + 1


def _incr_left(num1, num2):
    return num1 + 1


def ancestors(tree):
    """Compute the number of ancestors in a tree."""
    return tree.map(fun.zero, fun.zero) \
        .dacc(_incr, _incr, 0, fun.idt, fun.idt, _incr, _incr)


def diameter(tree):
    """Compute the size of the longest path in a tree, also called diameter"""
    return tree.map(fun.zero, fun.zero) \
        .dacc(_incr, _incr, 0, fun.idt, fun.idt, _incr, _incr) \
        .reduce(fun.max3, fun.idt, fun.max3, fun.max3, fun.max3)


def size(tree):
    """Return the size of the tree"""
    mapped_one = tree.map(fun.one, fun.one)
    return mapped_one.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add)


def sum_values(tree):
    """Return the sum of of values in the tree."""
    return tree.reduce(fun.add, fun.idt, fun.add, fun.add, fun.add)


def size_by_node(tree):
    """Return the size of the tree"""
    tree_mapped = tree.map(fun.one, fun.one)
    return tree_mapped.uacc(fun.add, fun.idt, fun.add, fun.add, fun.add)


def _k(left, _, right):
    (_, left) = left
    (_, right) = right
    return left, left + 1 + right


def _psi_n(left, node_value, right):
    (__, left) = left
    (nv0, nv1, nv2, nv3) = node_value
    (__, right) = right
    res_1 = nv0 * left + nv1 * (left + right + 1) + nv2
    res_2 = left + right + nv3
    return res_1, res_2


def _psi_l(left, node_value, right):
    (_, _, _, left) = left
    (nv0, nv1, nv2, nv3) = node_value
    (_, right) = right
    res_0 = 0
    res_1 = nv0 + nv1
    res_2 = (nv0 + nv1) * left + nv1 * (1 + right) + nv2
    res_3 = left + 1 + right + nv3
    return res_0, res_1, res_2, res_3


def _psi_r(left, node_value, right):
    (_, left) = left
    (nv0, nv1, nv2, nv3) = node_value
    (_, _, _, right) = right
    res_0 = 0
    res_1 = nv1
    res_2 = nv1 * right + nv0 * left + nv1 * (1 + left) + nv2
    res_3 = right + 1 + left + nv3
    return res_0, res_1, res_2, res_3


def _g_left(num, _):
    return num + 1


def _g_right(value, node_value):
    (left, _) = node_value
    return value + left + 1


def _phi_l(_):
    return 1


def _phi_r(node_value):
    (left, _) = node_value
    return left + 1


def _zero_one(_):
    return 0, 1


def _zero(_):
    return 0


def _phi(_):
    return 1, 0, 0, 1


def prefix(tree):
    """Return the prefix tree"""
    mapped = tree.map(_zero_one, fun.idt)
    tree2 = mapped.uacc(_k, _phi, _psi_n, _psi_l, _psi_r)
    return tree2.dacc(_g_left, _g_right, 0, _phi_l, _phi_r, add, add)


def depth(tree):
    """Return the deepth of each node"""
    return tree.dacc(_incr_left, _incr_left, 0, _zero, _zero, _incr, _incr)


def lca(t, a, b):
    """Lowest common ancestor"""
    pg = lambda x: (x == a or x == b, x)
    pg2 = lambda x: x[0] == a or x[0] == b
    tree = t.map(pg, pg)

    def flca(l, n, r):
        return (n[0] or l[0] or r[0]), n[1]

    def fpath(c, x):
        return c + [x[1]] if x[0] else []

    def unif(b1, b2):
        return [b1[1], b2[1]] if b1[0] and b2[0] else []

    tree = tree.uacc(flca, fun.idt, flca, flca, flca)
    res = t.zip(tree.dacc(fpath, fpath, [], fun.idt, fun.idt, fpath, unif))
    res = res.get_all(pg2)

    if res.length() > 2:
        raise Exception("IDs are not unique")
    if res.length() < 2:
        raise Exception("given IDs are not available")
    return [i for i, j in zip(res[0][1], res[1][1]) if i == j][0]


def l_ancestors(t):

    def fpath(anc, v):
        return anc + [v]

    ances = t.dacc(fpath, fpath, [], fun.idt, fun.idt, fpath, fpath)
    return t.zip(ances)


def lca2(t, a, b):
    """Lowest common ancestor, more costly version"""
    res = l_ancestors(t).get_all(lambda x: x[0] == a or x[0] == b)

    # if res.length() > 2:
    #     raise Exception("IDs are not unique")
    # if res.length() < 2:
    #     raise Exception("given IDs are not available")

    return [i for i, j in zip(res[0][1], res[1][1]) if i == j][0]
