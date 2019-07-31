"""
Tests for term rewriting systems
"""

import pytest
from pyske.core.opt.terms import Var, Term, subst, merge


def test_str_non_static():
    # pylint: disable=missing-docstring
    res = str(Term('f', [Var('x'), 2, 3], False))
    exp = "f(x, 2, 3)"
    assert res == exp


def test_str_static():
    # pylint: disable=missing-docstring
    res = str(Term('f', [Var('x'), 2, 3], True))
    exp = "[static]f(x, 2, 3)"
    assert res == exp


def test_str_raw():
    # pylint: disable=missing-docstring
    res = str(Term('__raw__', [[1, 2]]))
    exp = "RAW(<class 'list'>)"
    assert res == exp


def test_subst_python_const():
    # pylint: disable=missing-docstring
    res = subst(42, {'x': 11})
    exp = 42
    assert res == exp


def test_subst_var_ok():
    # pylint: disable=missing-docstring
    res = subst(Var('x'), {'x': 11})
    exp = 11
    assert res == exp


def test_subst_other_var():
    # pylint: disable=missing-docstring
    res = subst(Var('y'), {'x': 11})
    exp = Var('y')
    assert res == exp


def test_subst_term():
    # pylint: disable=missing-docstring
    res = subst(Term('f', [Var('x'), 2, 3], False), {'x': 11})
    exp = Term('f', [11, 2, 3], False)
    assert not exp.match(res)


def test_match_pattern_var():
    # pylint: disable=missing-docstring
    term = Term('f', [Var('x'), 2, 3], False)
    res = term.match(Var('Y'))
    exp = {'Y': term}
    assert res == exp


def test_merge():
    # pylint: disable=missing-docstring
    with pytest.raises(Exception):
        merge({'x': 1}, {'x': 2})
