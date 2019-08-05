"""
Module of basic function for composition optimization.
"""
__all__ = ['Fun', 'idt', 'compose', 'curry', 'uncurry']

from pyske.core.opt.terms import Var, Term, RULES_DB, Rule
from pyske.core.util import fun
from pyske.core.util.fun import idt


class Fun(Term):
    """Terms representing basic functions"""

    def __init__(self, fun_f, a, s=True):
        Term.__init__(self, fun_f, a, s)


def compose(fun_f, fun_g):
    """Function composition"""
    return Fun(fun.compose, [fun_f, fun_g])


def curry(fun_f):
    """Currying"""
    return Fun(fun.curry, [fun_f])


def uncurry(fun_f):
    """Uncurrying"""
    return Fun(fun.uncurry, [fun_f])


_IDT_COMPOSE_LEFT = \
    Rule(left=compose(idt, Var('fun_f')),
         right=Var('fun_f'),
         name="idt neutral compose left",
         type=Fun
         )

_IDT_COMPOSE_RIGHT = \
    Rule(left=compose(Var('fun_f'), idt),
         right=Var('fun_f'),
         name="idt neutral compose right",
         type=Fun
         )

_CURRY_UNCURRY = \
    Rule(left=curry(uncurry(Var('fun_f'))),
         right=Var('fun_f'),
         name="curry uncurry simplification",
         type=Fun)

RULES_DB.extend([_CURRY_UNCURRY, _IDT_COMPOSE_LEFT, _IDT_COMPOSE_RIGHT])
