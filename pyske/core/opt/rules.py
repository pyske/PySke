from pyske.core.opt.term import Var, Term, subst
from collections import namedtuple
import functools
from pyske.core.opt.util import merge

Rule = namedtuple('Rule', 'left right name')


def apply_rule(t: Term, r: Rule):
    substitution = t.match(r.left)
    if substitution is None:
        return t
    else:
        return subst(r.right, substitution)

def apply_rules(t: Term, rules):
    return functools.reduce(apply_rule, rules, t)

def compose(f, g):
    return lambda x: f(g(x))

map_map_rule = \
    Rule(left=Term('map', [Term('map', [Var('PL'), Var('f')]), Var('g')]),
         right=Term('map', [Var('PL'), Term(compose, [Var('f'), Var('g')])]),
         name="map map")

map_reduce_rule = \
    Rule(left=Term('reduce', [Term('map', [Var('PL'), Var('f')]), Var('op')]),
         right=Term('map_reduce', [Var('PL'), Var('f'), Var('op')]),
         name = "map reduce")

map_map_reduce_rule = \
    Rule(left=Term('map_reduce', [Term('map', [Var('PL'), Var('f')]), Var('g'), Var('op')]),
         right=Term('map_reduce', [Var('PL'), Term(compose, [Var('f'), Var('g')]), Var('op')]),
         name = "map map_reduce")

rules = [map_map_rule, map_reduce_rule, map_map_reduce_rule]

def inner_most_strategy(t: Term):
    condition = True
    prev_args = t.arguments
    while condition:
        new_args = [inner_most_strategy(e) if isinstance(e, Term) else e for e in prev_args]
        matches = [new_args[i].match(prev_args[i])
                   if isinstance(prev_args[i],  Term) else {} for i in range(0, len(new_args))]
        changes = functools.reduce(merge, matches, {})
        condition = changes != {}
        prev_args = new_args
    new_t = apply_rules(Term(t.function, new_args, t.static), rules)
    return new_t
