"""
Terms representing list expressions
"""
import importlib
import operator
from abc import ABC, abstractmethod

from pyske.core.opt.fun import compose, curry
from pyske.core.opt.terms import MODULES, Var, Term, RULES_DB, Rule

MODULES.update({'PList': importlib.import_module('pyske.core.list.plist')})
MODULES.update({'SList': importlib.import_module('pyske.core.list.slist')})

__all__ = ['PList', 'SList']


class _List(ABC):
    """List interface."""
    @staticmethod
    @abstractmethod
    def raw(lst):
        """Wrap a concrete list object"""

    @staticmethod
    @abstractmethod
    def init(value_at, size):
        """Return a list from an initialization function"""

    @abstractmethod
    def __getattr__(self, item):
        """Catch method calls"""


class PList(Term, _List):
    """Representation of parallel lists."""
    def __init__(self, f_symb='__init__', args=None, is_static=True):
        if args is None:
            args = ['PList']
        Term.__init__(self, f_symb, args, is_static)

    @staticmethod
    def raw(lst):
        return PList("__raw__", [lst])

    @staticmethod
    def init(value_at, size):
        return PList('init', ['PList', value_at, size])

    def __getattr__(self, item):
        def call_f(*args):
            return PList(item, [self] + list(args), False)

        return call_f


class SList(Term, _List):
    """Representation of sequential lists."""
    def __init__(self, f='__init__', a=None, s=True):
        if a is None:
            a = ['SList']
        Term.__init__(self, f, a, s)

    @staticmethod
    def raw(lst):
        return PList("__raw__", [lst])

    @staticmethod
    def init(value_at, size):
        return SList('init', ['SList', value_at, size])

    def __getattr__(self, item):
        def call_f(*args):
            return SList(item, [self] + list(args), False)

        return call_f


_MAP_MAP = \
    Rule(left=Term('map', [Term('map', [Var('PL'), Var('f')]), Var('g')], False),
         right=Term('map', [Var('PL'), compose(Var('f'), Var('g'))], False),
         name="map map",
         type=_List)

_MAP_REDUCE = \
    Rule(left=Term('reduce', [Term('map', [Var('PL'), Var('f')]), Var('binary_op')], False),
         right=Term('map_reduce', [Var('PL'), Var('f'), Var('binary_op')], False),
         name="map reduce",
         type=_List)

_ZIP_MAP = \
    Rule(left=Term('map', [Term('zip', [Var('PL1'), Var('PL2')]), Var('f')], False),
         right=Term('map2', [Var('PL1'), curry(Var('f')), Var('PL2')], False),
         name="zip_map",
         type=_List)

_MAP_REDUCE_NEUTRAL = \
    Rule(left=Term('reduce',
                   [Term('map', [Var('PL'), Var('f')]), Var('binary_op'), Var('e')], False),
         right=Term('map_reduce', [Var('PL'), Var('f'), Var('binary_op'), Var('e')], False),
         name="map reduce",
         type=_List)

_AND_NOT_NOT_OR = \
    Rule(left=Term('reduce', [Term('map', [Var('list'), operator.not_, ]), operator.and_, True]),
         right=Term(operator.not_, [Term('reduce', [Var('list'), operator.or_, False])]),
         name="and not not or",
         type=_List)

RULES_DB.extend([_AND_NOT_NOT_OR, _MAP_REDUCE_NEUTRAL,
                 _MAP_REDUCE, _ZIP_MAP, _MAP_MAP])
