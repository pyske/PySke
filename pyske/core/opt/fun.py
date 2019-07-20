from pyske.core.opt.term import Var, Term
from pyske.core.opt.rules import inner_most_strategy, Rule, rules
import pyske.core.opt.util as util


class Fun(Term):

    def __init__(self, f, a, s=True):
        self.static = s
        self.function = f
        self.arguments = a

    def opt(self):
        return inner_most_strategy(self)

    def run(self):
        return self.opt().eval()


id = util.id


def compose(f, g):
    return Fun(util.compose, [f, g])


def curry(f):
    return Fun(util.curry, [f])


def uncurry(f):
    return Fun(util.uncurry, [f])

id_neutral_compose_left = \
    Rule(left=compose(id, Var('f')),
         right=Var('f'),
         name="id neutral compose left",
         type=Fun
         )

id_neutral_compose_right = \
    Rule(left=compose(Var('f'), id),
         right=Var('f'),
         name="id neutral compose right",
         type=Fun
         )

curry_uncurry_simplification = \
    Rule(left=curry(uncurry(Var('f'))),
         right=Var('f'),
         name="curry uncurry simplification",
         type=Fun)

rules.extend([curry_uncurry_simplification, id_neutral_compose_left, id_neutral_compose_right])
