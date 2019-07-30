"""
Term rewriting systems
"""
import functools
from functools import reduce
from collections import namedtuple
import types

__all__ = ['MODULES', 'Var', 'Term', 'Rule', 'RULES_DB']

MODULES = {}
RULES_DB = []


class Var(str):
    """Representation of term variables"""


class Term:
    """Representation of terms."""

    def __init__(self, f, a, s=False):
        self.static = s
        self.function = f
        self.arguments = a

    def eval(self):
        """Evaluate a term."""
        vargs = [e.eval() if issubclass(type(e), Term) else e for e in self.arguments]
        if isinstance(self.function,
                      (types.FunctionType, types.BuiltinFunctionType, functools.partial)):
            return self.function(*vargs)
        if self.function == "__raw__":
            return self.arguments[0]
        # arguments is assumed to be non-empty: it is either the class or object
        # to which the function/method is applied
        ocn = vargs.pop(0)
        # Getting the class or object
        if self.static:
            cls_obj = getattr(MODULES[ocn], ocn)
        else:
            cls_obj = ocn
        if self.function == '__init__':
            return cls_obj(*vargs)
        return getattr(cls_obj, self.function)(*vargs)

    def opt(self):
        """Optimized a term."""
        return inner_most_strategy(self)

    def run(self):
        """Execute an optimized term."""
        return self.opt().eval()

    def graft(self, pos, term):
        """Graft a term at a given position."""
        i = pos.pop(0)
        if not pos:
            self.arguments[i] = term
        else:
            self.arguments[i].graft(pos, term)

    @staticmethod
    def __match(obj, pattern):
        if isinstance(pattern, Var):
            return {pattern: obj}
        if isinstance(obj, Term):
            return obj.match(pattern)
        if obj == pattern:
            return {}
        return None

    def match(self, pattern):
        """Pattern-match a term against a pattern."""
        if isinstance(pattern, Var):
            substitution = {pattern: self}
        elif isinstance(pattern, Term) and self.function == pattern.function \
                and len(self.arguments) == len(pattern.arguments):
            terms = [Term.__match(self.arguments[idx], pattern.arguments[idx])
                     for idx in range(0, len(self.arguments))]
            substitution = reduce(merge, terms)
        else:
            substitution = None
        return substitution

    def __str__(self):
        if self.function == "__raw__":
            return "RAW(" + str(type(self.arguments[0])) + ")"
        args = reduce(lambda x, y: x + ", " + y, map(str, self.arguments))
        return ("[static]" if self.static else "") + str(self.function) + "(" + args + ")"


def subst(term, substitution):
    """Term substitution."""
    if isinstance(term, Var) and term in substitution:
        return substitution[term]
    if isinstance(term, Term):
        return type(term)(term.function,
                          [subst(e, substitution) for e in term.arguments],
                          term.static)
    return term


def merge(dict1: dict, dict2: dict):
    """Merge two disjoint dictionaries."""
    if dict1 is None or dict2 is None:
        return None
    keys1 = dict1.keys()
    keys2 = dict2.keys()
    if keys1 & keys2 != set():
        raise Exception("Non linear patterns not supported")
    dict_r = {k: dict1[k] for k in keys1}
    dict_r.update({k: dict2[k] for k in keys2})
    return dict_r


Rule = namedtuple('Rule', 'left right name type')


def apply_rule(term: Term, rule: Rule):
    """Apply a rule to a term."""
    if isinstance(term, rule.type):
        substitution = term.match(rule.left)
        if substitution is not None:
            new_t = subst(rule.right, substitution)
            if isinstance(new_t, Term):
                new_t = term.__class__(new_t.function, new_t.arguments, new_t.static)
            return new_t
    return term


def apply_rules(term: Term, rules):
    """Apply rules to a term."""
    return functools.reduce(apply_rule, rules, term)


def inner_most_strategy(term: Term):
    """Apply all available rules on a term (inner most strategy)."""
    if term.function == "__raw__":
        return term
    condition = True
    prev_args = term.arguments
    new_args = []
    while condition:
        new_args = [inner_most_strategy(e) if isinstance(e, Term) else e for e in prev_args]
        matches = [new_args[i].match(prev_args[i])
                   if isinstance(new_args[i], Term) else {} for i in range(0, len(new_args))]
        changes = functools.reduce(merge, matches, {})
        condition = changes != {}
        prev_args = new_args
    new_t = type(term)(term.function, new_args, term.static)
    new_t = apply_rules(new_t, RULES_DB)
    if isinstance(new_t, Term):
        if new_t.match(term) == {}:
            return new_t
        return inner_most_strategy(new_t)
    return new_t
