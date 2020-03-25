from pyske.core import interface

from typing import TypeVar, Callable, Optional, List, Tuple

from pyske.core.tree.ptree import PTree
from pyske.core.tree.ltree import LTree
from pyske.core.tree.rbtree import RBTree
from pyske.core.tree.rltree import RLTree
from pyske.core.tree.rtree import RTree
from pyske.core.util import fun

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name

__all__ = ['RPTree']


class RPTree(interface.RoseTree):

    def __init__(self, a):
        self.__pt = a

    def __str__(self):
        return str(self.__pt)

    def __eq__(self, other):
        if isinstance(other, RPTree):
            return self.__pt == other.__pt
        return False

    @staticmethod
    def from_rt(rt: 'RTree[A]', m=1):
        pt = PTree.from_bt(RBTree.from_rt(rt).bt, m)
        return RPTree(pt)

    def to_rt(self: 'RPTree[A]') -> 'RTree[A]':
        return RBTree(self.__pt.to_bt()).to_rt()

    @staticmethod
    def from_seq(rt: 'RLTree[A]') -> 'RPTree[A]':
        pt = PTree.from_lt(rt.lt)
        return RPTree(pt)

    def to_seq(self: 'RPTree[A]') -> 'RLTree[A]':
        lt = self.__pt.to_seq()
        return RLTree(lt)

    def map(self: 'RPTree[A]', k: Callable[[A], B]) -> 'RPTree[B]':
        return RPTree(self.__pt.map(lambda x: None, k))

    def map2(self: 'RPTree[A]', k: Callable[[A, B], C], a_rtree: 'RPTree[B]') -> 'RPTree[Tuple[A, B]]':
        return RPTree(self.__pt.map2(lambda x, y: None, k, a_rtree.__pt))

    def zip(self: 'RPTree[A]', a_rtree: 'RPTree[B]') -> 'RPTree[Tuple[A, B]]':
        return self.map2(lambda x, y: (x, y), a_rtree)

    def reduce(self: 'RPTree[A]',
               oplus: Callable[[A, B], B], unit_oplus: B,
               otimes: Callable[[B, B], B], unit_otimes: B) -> B:
        psi_n, phi, psi_l, psi_r = RPTree._get_upward_closure(oplus, unit_oplus, otimes, unit_otimes)
        return self.__pt.map(lambda x: unit_otimes, fun.idt)\
            .reduce(lambda l, n, r: otimes(oplus(n, l), r), phi, psi_n, psi_l, psi_r)

    def uacc(self: 'RPTree[A]',
             oplus: Callable[[A, B], B], unit_oplus: B,
             otimes: Callable[[B, B], B], unit_otimes: B) -> 'RPTree[B]':
        psi_n, phi, psi_l, psi_r = RPTree._get_upward_closure(oplus, unit_oplus, otimes, unit_otimes)
        bt2 = self.__pt.\
            map(lambda x: unit_otimes, fun.idt).\
            uacc(lambda l, n, r: otimes(oplus(n, l), r), phi, psi_n, psi_l, psi_r)
        return RPTree(self.__pt.map2(lambda l, r: None, lambda l, r: oplus(l, r), bt2.getchl(None)))

    def dacc(self: 'RPTree[A]', oplus: Callable[[A, A], A], unit: A) -> 'RPTree[A]':
        return RPTree(self.__pt.dacc(lambda c, n: oplus(c, n), lambda c, n: c, unit,
                                     fun.idt, lambda x: unit, oplus, oplus))

    # TODO: first from RLTree ! Then same implem, but using RPTree instances
    #   - lacc(self: 'RLTree[A]', oplus: Callable[[A, A], A], unit: A) -> 'RLTree[A]'
    #   - racc(self: 'RBTree[A]', oplus: Callable[[A, A], A], unit: A) -> 'RBTree[A]'

    def get_one(self: 'RPTree[A]', p: Callable[[A], bool]) -> Optional[A]:
        return self.__pt.get_one_node(p)

    def get_all(self: 'RPTree[A]', p: Callable[[A], bool]) -> List[A]:
        return self.__pt.get_all_nodes(p)
