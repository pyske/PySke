from pyske.core import interface
from pyske.core.tree.rtree import RTree
from pyske.core.util import fun

from pyske.core.tree.tag import Tag

from pyske.core.tree.ltree import LTree
from pyske.core.tree.rbtree import RBTree

from typing import TypeVar, Callable, Optional, List, Tuple

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name

__all__ = ['RLTree']


class RLTree(interface.RoseTree):

    def __init__(self, a):
        self.__lt = a

    def __str__(self):
        return str(self.__lt)

    def __eq__(self, other):
        if isinstance(other, RLTree):
            return self.__lt == other.__lt
        return False

    @property
    def lt(self):
        return self.__lt

    @staticmethod
    def from_rt(rt: RTree[A], m: int = 1, ftag=Tag.mbridge):
        return RLTree(LTree.from_bt(RBTree.from_rt(rt).bt, m, ftag))

    def to_rt(self):
        return RBTree(self.__lt.to_bt()).to_rt()

    def map(self: 'RLTree[A]', k: Callable[[A], B]) -> 'RLTree[B]':
        return RLTree(self.__lt.map(lambda x: None, k))

    def map2(self: 'RLTree[A]', k: Callable[[A, B], C], a_rtree: 'RLTree[B]') -> 'RLTree[Tuple[A, B]]':
        return RLTree(self.__lt.map2(lambda x, y: None, k, a_rtree.__lt))

    def zip(self: 'RLTree[A]', a_rtree: 'RLTree[B]') -> 'RLTree[Tuple[A, B]]':
        return self.map2(lambda x, y: (x, y), a_rtree)

    def reduce(self: 'RLTree[A]',
               oplus: Callable[[A, B], B], unit_oplus: B,
               otimes: Callable[[B, B], B], unit_otimes: B) -> B:
        psi_n, phi, psi_l, psi_r = RLTree._get_upward_closure(oplus, unit_oplus, otimes, unit_otimes)
        return self.__lt.map(lambda x: unit_otimes, fun.idt)\
            .reduce(lambda l, n, r: otimes(oplus(n, l), r), phi, psi_n, psi_l, psi_r)

    def uacc(self: 'RLTree[A]',
             oplus: Callable[[A, B], B], unit_oplus: B,
             otimes: Callable[[B, B], B], unit_otimes: B) -> 'RLTree[B]':
        psi_n, phi, psi_l, psi_r = RLTree._get_upward_closure(oplus, unit_oplus, otimes, unit_otimes)
        bt2 = self.__lt.\
            map(lambda x: unit_otimes, fun.idt).\
            uacc(lambda l, n, r: otimes(oplus(n, l), r), phi, psi_n, psi_l, psi_r)
        return RLTree(self.__lt.map2(lambda l, r: None, lambda l, r: oplus(l, r), bt2.getchl(None)))

    def dacc(self: 'RLTree[A]', oplus: Callable[[A, A], A], unit: A) -> 'RLTree[A]':
        return RLTree(self.__lt.dacc(lambda c, n: oplus(c, n), lambda c, n: c, unit,
                                     fun.idt, lambda x: unit, oplus, oplus))

    # TODO
    # def lacc(self: 'RLTree[A]', oplus: Callable[[A, A], A], unit: A) -> 'RLTree[A]':
    #     psi_n, phi, psi_l, psi_r = RLTree._get_leftward_closure(oplus, unit)
    #     bt = self.__lt.map(lambda x: unit, fun.idt)
    #     return RLTree(bt.uacc(lambda l, n, r: oplus(n, r), phi, psi_n, psi_l, psi_r).getchr(None))

    # TODO
    # def racc(self: 'RBTree[A]', oplus: Callable[[A, A], A], unit: A) -> 'RBTree[A]':
    #
    #     def otimes(t1, t2):
    #         f1, p1, a1, b1 = t1
    #         f2, p2, a2, b2 = t2
    #         if f1 and f2:
    #             return True, \
    #                    p1 and p2, \
    #                    oplus(a1, a2), \
    #                    oplus(b1, a2) if p2 else b2
    #         elif f1:
    #             return t1
    #         else:
    #             return t2
    #
    #     def k(x):
    #         f, p, a, b = x
    #         return a if p else b
    #
    #     gl = lambda c, n: otimes(c, (True, False, n, unit))
    #     gr = lambda c, n: otimes(c, (True, True, n, unit))
    #     unit_otimes = False, True, unit, None
    #
    #     return RBTree(self.__bt.dacc(gl, gr, unit_otimes).map(lambda x: None, k))

    def get_one(self: 'RLTree[A]', p: Callable[[A], bool]) -> Optional[A]:
        return self.__lt.get_one_node(p)

    def get_all(self: 'RLTree[A]', p: Callable[[A], bool]) -> List[A]:
        return self.__lt.get_all_nodes(p)
