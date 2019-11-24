from abc import abstractmethod
from typing import TypeVar, Callable, Tuple, Generic, Union
from pyske.core import interface
from pyske.core.util.fun import up_div, dist_euclidean

__all__ = ['BTree', 'Node', 'Leaf', 'TAG_LEAF', 'TAG_NODE', 'TAG_CRITICAL']

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name
D = TypeVar('D')  # pylint: disable=invalid-name
U = TypeVar('U')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name



class BTree(interface.BinTree, Generic[A, B]):
    """An abstract class used to represent a Binary Tree"""

    @property
    def is_leaf(self: 'BTree[A, B]') -> bool:
        """ Indicates if the BTree is a leaf
        """
        return False

    @property
    def is_node(self: 'BTree[A, B]') -> bool:
        """ Indicates if the BTree is a node
        """
        return False

    @property
    @abstractmethod
    def value(self: 'BTree[A, B]') -> Union[A, B]:
        """
        :return: the top value of the current tree
        """

class Leaf(BTree):
    # pylint: disable=too-many-public-methods
    """
    Sequential leaf.

    Methods from interface BinTree:
        init_from_bt,
        size, map, zip, map2,
        reduce, uacc, dacc

    Methods from abstract BTree:
        is_leaf, is_node

    Methods:
        getchl, getchr
    """

    def __init__(self, a: A):
        self.__value = a
        self.__size = 1

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.value == other.value
        else:
            return False

    def _get_string(self, depth=0):
        return ("  "*depth) +"Leaf("+str(self.__value)+")"

    def __str__(self):
        return self._get_string()

    @property
    def size(self: 'BTree[A, B]') -> int:
        """Return the size of the tree"""
        return self.__size

    @property
    def value(self: 'BTree[A, B]') -> A:
        return self.__value

    @property
    def is_leaf(self: 'BTree[A, B]') -> bool:
        return True

    def map(self: 'BTree[A, B]', kl: Callable[[A], C], kn: Callable[[B], D]) -> 'BTree[C, D]':
        return Leaf(kl(self.value))

    def zip(self: 'BTree[A, B]', a_bintree: 'BTree[C, D]') -> 'BTree[Tuple[A, C], Tuple[B, D]]':
        assert a_bintree.is_leaf, "A leaf can only be zipped with another leaf"
        return Leaf((self.value, a_bintree.value))

    def map2(self: 'BTree[A, B]', kl: Callable[[A, C], U], kn: Callable[[B, D], V],
             a_bintree: 'BTree[C, D]') -> 'BTree[U, V]':
        assert a_bintree.is_leaf, "A leaf can only be zipped with another leaf"
        return Leaf(kl(self.value, a_bintree.value))

    def reduce(self: 'BTree[A, B]', k: Callable[[A, B, A], A],
               phi: Callable[[B], C] = None,
               psi_n: Callable[[A, C, A], A] = None,
               psi_l: Callable[[C, C, A], C] = None,
               psi_r: Callable[[A, C, C], C] = None
               ) -> A:
        return self.value

    def uacc(self: 'BTree[A, B]', k: Callable[[A, B, A], A],
             phi: Callable[[B], C] = None,
             psi_n: Callable[[A, C, A], A] = None,
             psi_l: Callable[[C, C, A], C] = None,
             psi_r: Callable[[A, C, C], C] = None
             ) -> 'BTree[A, A]':
        return Leaf(self.value)

    def dacc(self: 'BTree[A, B]', gl: Callable[[C, B], C], gr: Callable[[C, B], C], c: C,
             phi_l: Callable[[B], D] = None,
             phi_r: Callable[[B], D] = None,
             psi_u: Callable[[C, D], D] = None,
             psi_d: Callable[[C, D], C] = None
             ) -> 'BTree [C, C]':
        return Leaf(c)

    def getchl(self: 'BTree[A, A]', c: A) -> 'BTree[A, A]':
        return Leaf(c)

    def getchr(self: 'BTree[A, A]', c: A) -> 'BTree[A, A]':
        return Leaf(c)

    @staticmethod
    def init_from_bt(bt: 'BTree[A, B]', m: int = 1) -> 'BTree[A, B]':
        return Leaf(bt.value)


class Node(BTree):
    # pylint: disable=too-many-public-methods
    """
    Sequential node.

    Methods from interface BinTree:
        init_from_btree,
        size, right, left, map, zip, map2,
        reduce, uacc, dacc

    Methods from abstract BTree:
        is_leaf, is_node

    Methods:
        getchl, getchr
    """

    def __init__(self, b: B, left: 'Node[A, B]', right: 'Node[A, B]'):
        self.__value = b
        self.__left = left
        self.__right = right
        self.__size = 1 + left.size + right.size

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.value == other.value and self.left == other.left and self.right == other.right
        else:
            return False

    def _get_string(self, depth=0):
        res_l = self.__left._get_string(depth = depth + 1)
        res_r = self.__right._get_string(depth = depth + 1)
        return ("  "*depth) +"Node("+str(self.__value)+"\n" + res_l + "\n" + res_r + "\n" +("  "*depth) + ")"

    def __str__(self):
        return self._get_string()

    @property
    def size(self: 'BTree[A, B]') -> int:
        """Return the size of the tree"""
        return self.__size

    @property
    def left(self: 'BTree[A, B]') -> 'BTree[A, B]':
        """Return the left children of the node"""
        return self.__left

    @property
    def right(self: 'BTree[A, B]') -> 'BTree[A, B]':
        """Return the right children of the node"""
        return self.__right

    @property
    def value(self: 'BTree[A, B]') -> B:
        """Return the top value of the tree"""
        return self.__value

    @property
    def is_node(self: 'BTree[A, B]') -> bool:
        return True

    def map(self: 'BTree[A, B]', kl: Callable[[A], C], kn: Callable[[B], D]) -> 'BTree[C, D]':
        lm = self.left.map(kl, kn)
        rm = self.right.map(kl, kn)
        return Node(kn(self.value), lm, rm)

    def zip(self: 'BTree[A, B]', a_bintree: 'BTree[C, D]') -> 'BTree[Tuple[A, C], Tuple[B, D]]':
        assert a_bintree.is_node, "A node can only be zipped with another node"
        lz = self.left.zip(a_bintree.left)
        rz = self.right.zip(a_bintree.right)
        return Node((self.value, a_bintree.value), lz, rz)

    def map2(self: 'BTree[A, B]', kl: Callable[[A, C], U], kn: Callable[[B, D], V],
             a_bintree: 'BTree[C, D]') -> 'BTree[Tuple[A, C], Tuple[B, D]]':
        assert a_bintree.is_node, "A node can only be zipped with another node"
        lm = self.left.map2(kl, kn, a_bintree.left)
        rm = self.right.map2(kl, kn, a_bintree.right)
        return Node(kn(self.value, a_bintree.value), lm, rm)

    def reduce(self: 'BTree[A, B]', k: Callable[[A, B, A], A],
               phi: Callable[[B], C] = None,
               psi_n: Callable[[A, C, A], A] = None,
               psi_l: Callable[[C, C, A], C] = None,
               psi_r: Callable[[A, C, C], C] = None
               ) -> A:
        lr = self.left.reduce(k)
        rr = self.right.reduce(k)
        return k(lr, self.value, rr)

    def uacc(self: 'BTree[A, B]', k: Callable[[A, B, A], A],
             phi: Callable[[B], C] = None,
             psi_n: Callable[[A, C, A], A] = None,
             psi_l: Callable[[C, C, A], C] = None,
             psi_r: Callable[[A, C, C], C] = None
             ) -> 'BTree[A, A]':
        lu = self.left.uacc(k)
        ru = self.right.uacc(k)
        return Node(k(lu.value, self.value, ru.value), lu, ru)

    def dacc(self: 'BTree[A, B]', gl: Callable[[C, B], C], gr: Callable[[C, B], C], c: C,
             phi_l: Callable[[B], D] = None,
             phi_r: Callable[[B], D] = None,
             psi_u: Callable[[C, D], D] = None,
             psi_d: Callable[[C, D], C] = None
             ) -> 'BTree [C, C]':
        b = self.value
        ld = self.left.dacc(gl, gr, gl(c, b))
        rd = self.right.dacc(gl, gr, gr(c, b))
        return Node(c, ld, rd)

    def getchl(self: 'BTree[A, A]', c: A) -> 'BTree[A, A]':
        return Node(self.left.value, self.left.getchl(c), self.right.getchl(c))

    def getchr(self: 'BTree[A, A]', c: A) -> 'BTree[A, A]':
        return Node(self.right.value, self.left.getchr(c), self.right.getchr(c))

    @staticmethod
    def init_from_bt(bt: 'BTree[A, B]', m: int = 1) -> 'BTree[A, B]':
        li = BTree.init_from_bt(bt.left)
        ri = BTree.init_from_bt(bt.right)
        return Node(bt.value, li, ri)
