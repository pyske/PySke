from pyske.core.tree.btree import Node, Leaf
from pyske.core import interface, SList
from pyske.core.tree.rtree import RTree
from pyske.core.util import fun

from pyske.core.tree.btree import BTree, Node, Leaf
from typing import TypeVar, Generic, Callable, Union, Any


A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name


class RBTree(interface.RoseTree):

    def __init__(self, a):
        self.__bt = a

    def __str__(self):
        return str(self.__bt)

    def __eq__(self, other):
        if isinstance(other, RBTree):
            return self.__bt == other.__bt
        return False

    @staticmethod
    def from_rt(rt: RTree[A]):

        def r2b1(t, ss):
            left = r2b2(t.children)
            right = r2b2(ss)
            return Node(t.value, left, right)

        def r2b2(ts):
            if ts.empty():
                return Leaf(None)
            else:
                h = ts.head()
                t = ts.tail()
                return r2b1(h, t)

        return RBTree(r2b1(rt, SList()))

    def to_rt(self):

        def b2r(t) -> SList:
            if t.is_node:
                res_l = b2r(t.left)
                res_r = b2r(t.right)
                res_head = RTree(t.value, SList(res_l))
                res_r.insert(0, res_head)
                return res_r
            if t.is_leaf:
                return SList()

        # return b2r(self.__bt)
        return b2r(self.__bt).head()

    def map(self: 'RBTree[A]', k: Callable[[A], B]) -> 'RBTree[B]':
        return RBTree(self.__bt.map(lambda x: None, k))

    def map2(self: 'RBTree[A]', k: Callable[[A, B], C], a_rtree: 'RBTree[B]') -> 'RBTree[Tuple[A, B]]':
        return RBTree(self.__bt.map2(lambda x, y: None, k, a_rtree.__bt))

    def zip(self: 'RBTree[A]', a_rtree: 'RBTree[B]') -> 'RBTree[Tuple[A, B]]':
        return self.map2(lambda x, y: (x, y), a_rtree)

    def reduce(self: 'RBTree[A]',
               oplus: Callable[[A, B], B], unit_oplus: B,
               otimes: Callable[[B, B], B], unit_otimes: B) -> B:
        return self.__bt.map(lambda x: unit_otimes, fun.idt).reduce(lambda l, n, r: otimes(oplus(n, l), r))





