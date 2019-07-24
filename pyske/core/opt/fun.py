__all__ = ['Fun', 'idt', 'compose', 'curry', 'uncurry']

from pyske.core.opt.terms import Var, Term
from pyske.core.opt.rules import inner_most_strategy, Rule, rules
from pyske.core.util import fun


class Fun(Term):

    def __init__(self, f, a, s=True):
        Term.__init__(self, f, a, s)

    def opt(self):
        return inner_most_strategy(self)

    def run(self):
        return self.opt().eval()


idt = fun.idt


def compose(f, g):
    return Fun(fun.compose, [f, g])


def curry(f):
    return Fun(fun.curry, [f])


def uncurry(f):
    return Fun(fun.uncurry, [f])


id_neutral_compose_left = \
    Rule(left=compose(idt, Var('f')),
         right=Var('f'),
         name="idt neutral compose left",
         type=Fun
         )

id_neutral_compose_right = \
    Rule(left=compose(Var('f'), id),
         right=Var('f'),
         name="idt neutral compose right",
         type=Fun
         )

curry_uncurry_simplification = \
    Rule(left=curry(uncurry(Var('f'))),
         right=Var('f'),
         name="curry uncurry simplification",
         type=Fun)

rules.extend([curry_uncurry_simplification, id_neutral_compose_left, id_neutral_compose_right])
