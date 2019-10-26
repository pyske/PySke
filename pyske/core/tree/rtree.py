from typing import Generic, TypeVar, Callable, Any, Tuple

from pyske.core.list.slist import SList
from pyske.core.tree.btree import Node, Leaf, BTree

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name


class RNode (Generic[A]):

    def __init__(self, value, ts=None):
        self.__value = value
        if ts is None:
            self.__children = SList([])
        else:
            self.__children = SList(ts)

    @property
    def value(self) -> A:
        return self.__value

    @property
    def children(self) -> SList['RNode[A]']:
        return self.__children

    @staticmethod
    def init_from_bt(bt: 'BTree[A, A]') -> 'RNode[A]':

        def __aux(btree: 'BTree[A, A]') -> 'SList[RNode[A]]':
            if btree.is_leaf:
                if btree.value is None:
                    return SList()
                else:
                    return SList([RNode(btree.value)])
            else:
                res_l = __aux(btree.left)
                res_r = __aux(btree.right)
                res_head = RNode(btree.value, res_l)
                res_r.insert(0, res_head)
                return res_r

        return __aux(bt).head()

    def __str__(self: 'RNode[A]') -> str:
        res = "rnode " + str(self.value) + "["
        ch = self.children
        for i in range(0, ch.length()):
            if i == ch.length() - 1:
                res = res + str(ch[i])
            else:
                res = res + str(ch[i]) + ", "
        return res + "]"

    def __eq__(self: 'RNode[A]', other: Any) -> bool:
        if isinstance(other, RNode):
            ch1 = self.children
            ch2 = other.children
            if ch1.length() != ch2.length():
                return False
            for i in range(0, ch1.length()):
                if ch1[i] != ch2[i]:
                    return False
            return self.value == other.value
        return False

    def is_leaf(self: 'RNode[A]') -> bool:
        return len(self.children) == 0

    def is_node(self: 'RNode[A]') -> bool:
        return len(self.children) != 0

    def map(self: 'RNode[A]', f: Callable[[A], B]) -> 'RNode[B]':
        v = f(self.value)
        ch = self.children.map(lambda x: x.map(f))
        return RNode(v, ch)

    def reduce(self: 'RNode[A]', f: Callable[[A, B], B], g: Callable[[B, B], B]) -> B:
        if self.children.empty():
            return self.value
        # We calculate the reduction of each childen
        reductions = self.children.map(lambda x: x.reduce(f, g))
        # We combine every sub reductions using g
        red = reductions[0]
        for i in range(1, reductions.length()):
            red = g(red, reductions[i])
        # The final reduction is the result of the combination of sub reductions and the value of the current instance
        return f(self.value, red)

    def uacc(self: 'RNode[A]', f: Callable[[A, B], B], g: Callable[[B, B], B]) -> 'RNode[B]':
        v = self.reduce(f, g)
        ch = self.children.map(lambda x: x.uacc(f, g))
        return RNode(v, ch)

    def dacc(self: 'RNode[A]', f: Callable[[A, A], A], unit_f: A) -> 'RNode[A]':
        def __dacc_aux(t, fct, c):
            # Auxiliary function to make an accumulation with an arbitrary accumulator
            return RNode(c, t.children.map(lambda x: __dacc_aux(x, fct, fct(c, t.value))))
        # Since the accumulator changes at each iteration, we need to use a changing parameter, not defined in dacc.
        # Use of an auxiliary function, with as a first accumulator, unit_f
        return __dacc_aux(self, f, unit_f)

    def zip(self: 'RNode[A]', rt: 'RNode[B]') -> 'RNode[Tuple[A, B]]':
        ch1 = self.children
        ch2 = rt.children
        assert ch1.length() == ch2.length(), "The rose trees cannot be zipped (not the same shape)"
        ch = SList([])
        for i in range(0, ch1.length()):
            ch.append(ch1[i].zip(ch2[i]))
        v = (self.value, rt.value)
        return RNode(v, ch)

    def map2(self: 'RNode[A]', f: Callable[[A, B], C], rt: 'RNode[B]') -> 'RNode[C]':
        ch1 = self.children
        ch2 = rt.children
        assert ch1.length() == ch2.length(), "The rose trees cannot be zipped (not the same shape)"
        ch = SList([])
        for i in range(0, ch1.length()):
            ch.append(ch1[i].map2(f, ch2[i]))
        v = f(self.value, rt.value)
        return RNode(v, ch)

    def racc(self: 'RNode[A]', f: Callable[[A, A], A], unit_f: A) -> 'RNode[A]':
        rv = self.children.map(lambda x: x.value)
        rs = rv.scanl(f, unit_f)
        ch = SList()
        ch0 = self.children
        for i in range(ch0.length()):
            ch.append(RNode(rs[i], ch0[i].racc(f, unit_f).children))
        return RNode(unit_f, ch)

    def lacc(self: 'RNode[A]', f: Callable[[A, A], A], unit_f: A) -> 'RNode[A]':
        rv = self.children.map(lambda x: x.value)
        rs = rv.scanp(f, unit_f)
        ch = SList()
        ch0 = self.children
        for i in range(ch0.length()):
            ch.append(RNode(rs[i], ch0[i].lacc(f, unit_f).children))
        return RNode(unit_f, ch)

    def r2b(self: 'RNode[A]') -> BTree[A, B]:

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

        return r2b1(self, SList())
