from pyske.core.opt.term import modules, Var, Term
from pyske.core.opt.rules import inner_most_strategy, Rule, rules
from pyske.core.opt.fun import *
import importlib
import operator

modules.update({'PList': importlib.import_module('pyske.core.list.plist')})
modules.update({'SList': importlib.import_module('pyske.core.list.slist')})

class __List:
    pass


class PList(Term, __List):

    def __init__(self, f='__init__', a=['PList'], s=True):
        self.static = s
        self.function = f
        self.arguments = a

    @staticmethod
    def raw(l):
        return PList("__raw__", [l])

    @staticmethod
    def init(f, size):
        return PList('init', ['PList', f, size])

    def opt(self):
        return inner_most_strategy(self)

    def run(self):
        return self.opt().eval()

    def __getattr__(self, item):
        def f(*args):
            return PList(item, [self] + list(args), False)
        return f



class SList(Term, __List):

    def __init__(self, f='__init__', a=['SList'], s=True):
        self.static = s
        self.function = f
        self.arguments = a

    @staticmethod
    def raw(l):
        return PList("__raw__", [l])

    @staticmethod
    def init(f, size):
        return SList('init', ['SList', f, size])

    def run(self):
        opt = inner_most_strategy(self)
        return opt.eval()

    def __getattr__(self, item):
        def f(*args):
            return SList(item, [self] + list(args), False)
        return f


map_map_rule = \
    Rule(left=Term('map', [Term('map', [Var('PL'), Var('f')]), Var('g')], False),
         right=Term('map', [Var('PL'), compose(Var('f'), Var('g'))], False),
         name="map map",
         type=__List)


map_reduce_rule = \
    Rule(left=Term('reduce', [Term('map', [Var('PL'), Var('f')]), Var('op')], False),
         right=Term('map_reduce', [Var('PL'), Var('f'), Var('op')], False),
         name="map reduce",
         type=__List)

zip_map_rule = \
    Rule(left=Term('map', [Term('zip', [Var('PL1'), Var('PL2')]), Var('f')], False),
         right=Term('map2', [Var('PL1'), curry(Var('f')), Var('PL2')], False),
         name="zip_map",
         type=__List)


map_reduce_e_rule = \
    Rule(left=Term('reduce', [Term('map', [Var('PL'), Var('f')]), Var('op'), Var('e')], False),
         right=Term('map_reduce', [Var('PL'), Var('f'), Var('op'), Var('e')], False),
         name="map reduce",
         type=__List)


and_not_not_or_rule = \
    Rule(left=Term('reduce', [Term('map', [Var('list'), operator.not_,]), operator.and_, True]),
         right=Term(operator.not_, [Term('reduce', [Var('list'), operator.or_, False])]),
         name="and not not or",
         type=__List)

#
rules.extend([ and_not_not_or_rule, map_reduce_e_rule, map_reduce_rule, zip_map_rule, map_map_rule])
