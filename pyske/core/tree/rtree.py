from pyske.core.list.slist import SList
from pyske.core import interface

from typing import TypeVar, Callable, Generic, Any, Tuple

__all__ = ['RTree']

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name


class RTree(interface.RoseTree, Generic[A]):
    # pylint: disable=too-many-public-methods
    """
    PySke rose trees (interface)

    Methods from interface RoseTree:
        from_rt, to_rt
        size, map, zip, map2,
        reduce, uacc, dacc,
        lacc, racc

    Methods:
        is_leaf, is_node
    """

    def __init__(self, val, ch: SList = None):
        self.__value = val
        if ch is None:
            ch = SList()
        if not isinstance(ch, SList):
            ch = SList(ch)
        self.__children = ch
        self.__size = 1
        # for c in ch:
        #     self.__size += c.size

    @property
    def is_leaf(self: 'RTree[A]') -> bool:
        """ Indicates if the RTree is a leaf
        """
        return self.__children == SList()

    @property
    def is_node(self: 'RTree[A]') -> bool:
        """ Indicates if the RTree is a node
        """
        return self.__children != SList()

    @property
    def value(self: 'RTree[A]') -> A:
        """
        :return: the top value of the current tree
        """
        return self.__value

    @property
    def children(self: 'RTree[A]') -> 'SList[RTree[A]]':
        """
        :return: the childrens of the current tree
        """
        return self.__children

    @property
    def size(self: 'RTree[A]') -> int:
        return self.__size

    def __eq__(self: 'RTree[A]', other: Any) -> bool:
        if isinstance(other, RTree):
            ch1 = self.children
            ch2 = other.children
            if ch1.length() != ch2.length():
                return False
            for i in range(0, ch1.length()):
                if ch1[i] != ch2[i]:
                    return False
            return self.value == other.value
        return False

    def _get_string(self: 'RTree[A]', depth=0):
        res = ("  " * depth) + ("Leaf(" if self.is_leaf else "Node(") + str(self.value)
        if self.is_leaf:
            return ("  " * depth) + "Leaf(" + str(self.value) + ")"
        res = ("  " * depth) + "Node(" + str(self.value) + "\n"
        for i in range(self.children.length()):
            c = self.children[i]
            res = res + c._get_string(depth=depth + 1) + ("\n" if i != self.children.length()-1 else "")
        return res + "\n" + ("  " * depth) + ")"

    def __str__(self: 'RTree[A]') -> str:
        return self._get_string(depth=0)

    @staticmethod
    def from_rt(rt: 'RTree[A]') -> Any:
        new_ch = SList.init(lambda x: None, rt.children.length())
        for i in range(rt.children.length()):
            new_ch[i] = RTree.from_rt(rt.children[i])
        return RTree(rt.value, new_ch)

    def to_rt(self: 'RTree[A]') -> 'RTree[A]':
        new_ch = SList.init(lambda x: None, self.children.length())
        for i in range(self.children.length()):
            new_ch[i] = RTree.from_rt(self.children[i])
        return RTree(self.value, new_ch)

    def map(self: 'RTree[A]', k: Callable[[A], B]) -> 'RTree[B]':
        v = k(self.value)
        ch = self.children.map(lambda x: x.map(k))
        return RTree(v, ch)

    def zip(self: 'RTree[A]',
            a_rosetree: 'RTree[B]') -> 'RTree[Tuple[A, B]]':
        ch1 = self.children
        ch2 = a_rosetree.children
        assert ch1.length() == ch2.length(), "The rose trees cannot be zipped (not the same shape)"
        new_ch = SList.init(lambda x: None, ch1.length())
        for i in range(0, ch1.length()):
            new_ch[i] = ch1[i].zip(ch2[i])
        v = (self.value, a_rosetree.value)
        return RTree(v, new_ch)

    def map2(self: 'RTree[A]', k: Callable[[A, B], C],
             a_rosetree: 'RTree[B]') -> 'RTree[C]':
        ch1 = self.children
        ch2 = a_rosetree.children
        assert ch1.length() == ch2.length(), "The rose trees cannot be zipped (not the same shape)"
        new_ch = SList.init(lambda x: None, ch1.length())
        for i in range(0, ch1.length()):
            new_ch[i] = ch1[i].map2(k, ch2[i])
        v = k(self.value, a_rosetree.value)
        return RTree(v, new_ch)

    def reduce(self: 'RTree[A]',
               oplus: Callable[[A, B], B], unit_plus: B,
               otimes: Callable[[B, B], B], unit_otimes: B = None) -> B:
        if self.is_leaf:
            return self.value
        reductions = self.children.map(lambda x: x.reduce(oplus, unit_plus,
                                                          otimes, unit_otimes)
                                       )
        red = reductions.reduce(otimes, unit_otimes)
        return oplus(self.value, red)

    def uacc(self: 'RTree[A]',
             oplus: Callable[[A, B], B], unit_oplus: B,
             otimes: Callable[[B, B], B], unit_times: B) -> 'RTree[B]':
        if self.is_leaf:
            return RTree(self.value)
        new_ch = self.children.map(lambda x: x.uacc(oplus, unit_oplus,
                                                    otimes, unit_times))
        red = new_ch[0].value
        for i in range(1, len(new_ch)):
            red = otimes(red, new_ch[i].value)
        return RTree(oplus(self.value, red), new_ch)

    def dacc(self: 'RTree[A]', oplus: Callable[[A, A], A],
             unit: A) -> 'RTree[A]':
        def __dacc_aux(t, fct, c):
            new_ch = t.children.map(lambda x: __dacc_aux(x, fct, fct(c, t.value)))
            return RTree(c, new_ch)
        return __dacc_aux(self, oplus, unit)

    def lacc(self: 'RTree[A]', oplus: Callable[[A, A], A],
             unit: A) -> 'RTree[A]':
        rv = self.children.map(lambda x: x.value)
        rs = rv.scanp(oplus, unit)
        ch0 = self.children
        new_ch = SList.init(lambda x: None, ch0.length())
        for i in range(ch0.length()):
            new_ch[i] = RTree(rs[i], ch0[i].lacc(oplus, unit).children)
        return RTree(unit, new_ch)

    def racc(self: 'RTree[A]', oplus: Callable[[A, A], A],
             unit: A) -> 'RTree[A]':
        rv = self.children.map(lambda x: x.value)
        rs = rv.scanl(oplus, unit)
        ch0 = self.children
        new_ch = SList.init(lambda x: None, ch0.length())
        for i in range(ch0.length()):
            new_ch[i] = RTree(rs[i], ch0[i].racc(oplus, unit).children)
        return RTree(unit, new_ch)
