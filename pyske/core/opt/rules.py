from pyske.core.opt.term import Term, subst
from collections import namedtuple
import functools
from pyske.core.opt.util import merge

Rule = namedtuple('Rule', 'left right name type')


def apply_rule(t: Term, r: Rule):
    if isinstance(t, r.type):
        substitution = t.match(r.left)
        if not(substitution is None):
            new_t = subst(r.right, substitution)
            if isinstance(new_t, Term):
                new_t = t.__class__(new_t.function, new_t.arguments, new_t.static)
            return new_t
    return t


def apply_rules(t: Term, rules):
    return functools.reduce(apply_rule, rules, t)


rules = []


def inner_most_strategy(t: Term):
    if t.function == "__raw__":
        return t
    condition = True
    prev_args = t.arguments
    while condition:
        new_args = [inner_most_strategy(e) if isinstance(e, Term) else e for e in prev_args]
        matches = [new_args[i].match(prev_args[i])
                   if isinstance(new_args[i],  Term) else {} for i in range(0, len(new_args))]
        changes = functools.reduce(merge, matches, {})
        condition = changes != {}
        prev_args = new_args
    new_t = t.__class__(t.function, new_args, t.static)
    new_t = apply_rules(new_t, rules)
    if isinstance(new_t, Term):
        if new_t.match(t) == {}:
            return new_t
        else:
            return inner_most_strategy(new_t)
    else:
        return new_t