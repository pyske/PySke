"""
Functions on trees
"""
from operator import add
from pyske.core.util import fun

__all__ = ['size', 'size_by_node', 'sum_values', 'prefix', 'ancestors']


def _incr(num1, num2):
    return num1 + num2 + 1


def ancestors(tree):
    """Compute the number of ancestors in a tree."""
    return tree.map(fun.zero, fun.zero) \
        .dacc(_incr, _incr, 0, fun.idt, fun.idt, _incr, _incr)


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
    res_2 = left + 1 + right + nv3
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


def _phi(_):
    return 1, 0, 0, 1


def prefix(tree):
    """Return the prefix tree"""
    mapped = tree.map(_zero_one, fun.idt)
    tree2 = mapped.uacc(_k, _phi, _psi_n, _psi_l, _psi_r)
    return tree2.dacc(_g_left, _g_right, 0, _phi_l, _phi_r, add, add)
