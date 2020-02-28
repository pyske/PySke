"""
Terms representing bintree expressions
"""
import importlib
from abc import ABC, abstractmethod

from pyske.core.opt.fun import compose, curry
from pyske.core.opt.terms import MODULES, Var, Term, RULES_DB, Rule
from pyske.core.tree.tag import Tag

MODULES.update({'PTree': importlib.import_module('pyske.core.tree.ptree')})
MODULES.update({'LTree': importlib.import_module('pyske.core.tree.ltree')})

__all__ = ['LTree', 'PTree']


class _BinTree(ABC):
    """BinTree interface."""
    @staticmethod
    @abstractmethod
    def raw(bt):
        """Wrap a concrete BinTree object"""

    @abstractmethod
    def __getattr__(self, item):
        """Catch method calls"""

    @staticmethod
    @abstractmethod
    def from_bt(bt, m):
        """Return a bintree from a bt"""


class LTree(Term, _BinTree):
    """Representation of sequential lists."""
    def __init__(self, f_symbol='__init__', args=None, is_static=True):
        if args is None:
            args = ['LTree']
            if f_symbol != '__init__':
                args = args + [f_symbol]
                f_symbol = '__init__'
        Term.__init__(self, f_symbol, args, is_static)

    @staticmethod
    def raw(bt):
        return LTree("__raw__", [bt])

    @staticmethod
    def from_bt(bt, m, ftag=Tag.mbridge):
        return LTree('from_bt', ['LTree', bt, m, ftag])

    def __getattr__(self, item):
        def call_f(*args):
            return LTree(item, [self] + list(args), False)

        return call_f


class PTree(Term, _BinTree):
    """Representation of parallel lists."""
    def __init__(self, f_symb='__init__', args=None, is_static=True):
        if args is None:
            args = ['PTree']
        Term.__init__(self, f_symb, args, is_static)

    @staticmethod
    def raw(bt):
        return PTree("__raw__", [bt])

    @staticmethod
    def from_bt(bt, m, ftag=Tag.mbridge):
        return PTree('from_bt', ['PTree', bt, m, ftag])

    @staticmethod
    def from_seq(lt):
        return PTree('from_seq', ['PTree', lt])

    def __getattr__(self, item):
        def call_f(*args):
            return PTree(item, [self] + list(args), False)

        return call_f


_MAP_MAP = \
    Rule(left=Term('map', [Term('map', [Var('PL'), Var('fl'), Var('fn')]), Var('gl'), Var('gn')], False),
         right=Term('map', [Var('PL'), compose(Var('fl'), Var('gl')), compose(Var('fn'), Var('gn'))], False),
         name="map map",
         type=_BinTree)

_ZIP_MAP = \
    Rule(left=Term('map', [Term('zip', [Var('PT1'), Var('PT2')]), Var('gl'), Var('gn')], False),
         right=Term('map2', [Var('PT1'), curry(Var('fl')), curry(Var('gl'))], False),
         name="zip map",
         type=_BinTree)

_MAP_REDUCE = \
    Rule(left=Term('reduce', [Term('map', [Var('PL'), Var('fl'), Var('fn')]),
                              Var('k'), Var('phi'), Var('psi_n'), Var('psi_l'), Var('psi_r')], False),
         right=Term('map_reduce', [Var('PL'), Var('fl'), Var('fn'),
                                   Var('k'), Var('phi'), Var('psi_n'), Var('psi_l'), Var('psi_r')], False),
         name="map reduce",
         type=_BinTree)

_ZIP_REDUCE = \
    Rule(left=Term('reduce', [Term('zip', [Var('PT1'), Var('PT2')]),
                              Var('k'), Var('phi'), Var('psi_n'), Var('psi_l'), Var('psi_r')], False),
         right=Term('zip_reduce', [Var('PT1'), Var('PT2'),
                                   Var('k'), Var('phi'), Var('psi_n'), Var('psi_l'), Var('psi_r')]),
         name='zip_reduce',
         type=_BinTree)

_MAP2_REDUCE = \
    Rule(left=Term('reduce', [Term('map2', [Var('PT1'), Var('kl'), Var('kn'), Var('PT2')]),
                              Var('k'), Var('phi'), Var('psi_n'), Var('psi_l'), Var('psi_r')], False),
         right=Term('map2_reduce', [Var('PT1'), Var('kl'), Var('kn'), Var('PT2'),
                                    Var('k'), Var('phi'), Var('psi_n'), Var('psi_l'), Var('psi_r')]),
         name='map2_reduce',
         type=_BinTree)

_MAP2_MAP = \
    Rule(left=Term('map', [Term('map2', [Var('PT1'), Var('gl'), Var('gn'), Var('PT2')]),
                           Var('fl'), Var('fn')], False),
         right= Term('map2', [Var('PT1'),
                              compose(Var('fl'), Var('gl')),
                              compose(Var('fn'), Var('gn')),
                              Var('PT2')],
                     False),
         name="map2 map",
         type=_BinTree)

RULES_DB.extend([_MAP_MAP, _ZIP_MAP, _MAP_REDUCE, _ZIP_REDUCE, _MAP2_REDUCE, _MAP2_MAP])
