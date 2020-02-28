from pyske.core.tree.btree import Node, Leaf
from pyske.core import interface, SList
from pyske.core.tree.rtree import RTree
from pyske.core.util import fun

from pyske.core.tree.btree import BTree, Node, Leaf
from typing import TypeVar, Generic, Callable, Union, Any

from abc import abstractmethod, ABC

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name


class RBTree(interface.RoseTree, ABC):

    @abstractmethod
    def _b2r(self):
        pass

    @property
    def is_node(self: 'RNode[A, B]') -> bool:
        return False

    @property
    def is_leaf(self: 'RNode[A, B]') -> bool:
        return False


class RLeaf(RBTree, Leaf):

    def __init__(self, a):
        super().__init__(a)

    @property
    def is_leaf(self: 'RLeaf[A, B]') -> bool:
        return True

    @staticmethod
    def from_rt(rt) -> Any:
        return RNode.from_rt(rt)

    def _b2r(self) -> SList:
        if self.value is None:
            return SList()
        else:
            return SList([RTree(self.value)])

    def to_rt(self):
        res = self._b2r()
        return res.head()

    def map(self: 'RLeaf[A]', k: Callable[[A], B]) -> 'RLeaf[B]':
        return RLeaf(self.value)

    def map2(self: 'RLeaf[A]', k: Callable[[A, B], C],
             a_rosetree: 'RBTree[B]'):
        assert a_rosetree.is_leaf, "A leaf can only be zipped with another leaf"
        return RLeaf(None)

    def zip(self: 'RLeaf[A]', a_rosetree: 'RBTree[B]'):
        assert a_rosetree.is_leaf, "A leaf can only be zipped with another leaf"
        return RLeaf(None)


class RNode(RBTree, Node):

    def __init__(self, a, l, r):
        super().__init__(a, l, r)

    @property
    def left(self: 'RNode[A, B]') -> 'RBTree[A, B]':
        """Return the left children of the node"""
        return super().left

    @property
    def right(self: 'RNode[A, B]') -> 'RBTree[A, B]':
        """Return the right children of the node"""
        return super().right

    @property
    def value(self: 'RNode[A, B]') -> B:
        """Return the top value of the tree"""
        return super().value

    @property
    def is_node(self: 'RNode[A, B]') -> bool:
        return True

    @staticmethod
    def from_rt(rt: RTree[A]):

        def r2b1(t, ss):
            left = r2b2(t.children)
            right = r2b2(ss)
            return RNode(t.value, left, right)

        def r2b2(ts):
            if ts.empty():
                return RLeaf(None)
            else:
                h = ts.head()
                t = ts.tail()
                return r2b1(h, t)

        return r2b1(rt, SList())

    def _b2r(self) -> SList:
        res_l = self.left._b2r()
        res_r = self.right._b2r()
        res_head = RTree(self.value, SList([res_l]))
        res_r.insert(0, res_head)
        return res_r

    def to_rt(self):
        return self._b2r().head()

    def map(self: 'RNode[A]', k: Callable[[A], B]) -> 'RNode[B]':
        left = self.left.map(k)
        right = self.right.map(k)
        return RNode(k(self.value), left, right)

    def map2(self: 'Node[A]', k: Callable[[A, B], C],
             a_rosetree: 'RBTree[B]'):
        assert a_rosetree.is_node, "A leaf can only be zipped with another node"
        left = self.left.map2(k, a_rosetree.left)
        right = self.right.map2(k, a_rosetree.right)
        return RNode(k(self.value, a_rosetree.value), left, right)

    def zip(self: 'Node[A]', a_rosetree: 'RBTree[B]'):
        assert a_rosetree.is_node, "A leaf can only be zipped with another node"
        left = self.left.zip(a_rosetree.left)
        right = self.right.zip(a_rosetree.right)
        return RNode((self.value, a_rosetree.value), left, right)
