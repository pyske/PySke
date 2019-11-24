import sys
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable, Union, Tuple, Optional, Any
from pyske.core.tree.btree import BTree, Node, Leaf
from pyske.core.tree.tag import Tag, TAG_LEAF, TAG_NODE, TAG_CRITICAL

from pyske.core.util import fun
from pyske.core import interface, SList
from pyske.core.support.errors import IllFormedError, ApplicationError, NotSameTagError

__all__ = ['Segment', 'LTree']

MINUS_INFINITY = int((-sys.maxsize - 1) / 2)

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name
D = TypeVar('D')  # pylint: disable=invalid-name
U = TypeVar('U')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name


class __List(ABC, list):

    def length(self: '__List') -> int:
        return len(self)

    def empty(self: '__List') -> bool:
        return self == []

    @staticmethod
    @abstractmethod
    def init(value_at: Callable[[int], Any], size: int):
        pass


class Segment(__List, Generic[A, B]):
    # pylint: disable=too-many-public-methods
    """
    Linearized segment of tree.
    A list of pair (val, tag) of type union(A,B) * int

    Methods from abstract __List:
        init, length, empty

    Methods:
        has_critical, get_left, get_right,
        map_local, zip_local, map2_local,
        reduce_local, reduce_global,
        uacc_local, uacc_global, uacc_update,
        dacc_path, dacc_global, dacc_local
    """

    def __eq__(self: 'Segment[A, B]', other: Any) -> bool:
        if isinstance(other, Segment):
            if self.length() != other.length():
                return False
            for i in range(0, self.length()):
                if self[i] != other[i]:
                    return False
            return True
        return False

    def __str__(self):
        def __str_v(p):
            val, tag = p
            if tag is TAG_LEAF:
                return str(val)+"L"
            if tag is TAG_NODE:
                return str(val)+"N"
            if tag is TAG_CRITICAL:
                return str(val)+"C"
        res = "["
        for i in range(len(self)):
            res = res + __str_v(self[i]) + (',' if i != len(self) - 1 else '')
        res = res + "]"
        return res

    def empty(self: '__List') -> bool:
        return self == Segment()

    @staticmethod
    def init(value_at: Callable[[int], Any], size: int):
        assert size >= 0
        return Segment([value_at(i) for i in range(0, size)])

    def has_critical(self: 'Segment[A, B]') -> bool:
        for (val, tag) in self:
            if tag is TAG_CRITICAL:
                return True
        return False

    def get_left(self: 'Segment[A, B]', i: int) -> Union[A, B]:
        assert not self.has_critical(), "The left children of a value in a non-global Segment cannot be found"
        assert self[i][1] is not TAG_LEAF, "A leaf value doesn't have a left children"
        assert i < self.length() - 1, "Cannot get the left children of a node in an ill-formed Segment"
        return self[i + 1]

    def get_right(self: 'Segment[A, B]', i: int) -> Union[A, B]:
        assert not self.has_critical(), "The right children of a value in a non-global Segment cannot be found"
        assert self[i][1] is not TAG_LEAF, "A leaf value doesn't have a right children"
        assert i < self.length() - 2, "Cannot get the left children of a node in an ill-formed Segment"

        def get_right_index(gt, idx):
            _, tag = gt[idx + 1]
            if tag is TAG_LEAF:
                return idx + 2
            else:
                return 1 + get_right_index(gt, idx + 1)

        j = get_right_index(self, i)
        return self[j]

    # <editor-fold desc="Map functions">
    def map_local(self: 'Segment[A, B]', kl: Callable[[A], C], kn: Callable[[B], D]) -> 'Segment[C, D]':
        lgth = self.length()
        res = Segment.init(lambda idx: None, lgth)
        for i in range(lgth):
            (val, tag) = self[i]
            res[i] = kl(val) if tag is TAG_LEAF else kn(val), tag
        return res

    def zip_local(self: 'Segment[A, B]', seg: 'Segment[C, D]') -> 'Segment[Tuple[A, C], Tuple[B, D]]':
        lgth = self.length()
        assert lgth == seg.length(), "The linearized trees have not the same shape"
        res = Segment.init(lambda idx: None, lgth)
        for j in range(lgth):
            (val1, tag1) = self[j]
            (val2, tag2) = seg[j]
            if tag1 != tag2:
                raise NotSameTagError("Two zipped values have not the same tag")
            res[j] = ((val1, val2), tag1)
        return res

    def map2_local(self: 'Segment[A, B]', kl: Callable[[A, C], U],
                   kn: Callable[[B, D], V], seg: 'Segment[C, D]') -> 'Segment[U, V]':
        lgth = self.length()
        assert lgth == seg.length(), "The linearized trees have not the same shape"
        res = Segment.init(lambda idx: None, lgth)
        for j in range(lgth):
            (val1, tag1) = self[j]
            (val2, tag2) = seg[j]
            if tag1 != tag2:
                raise NotSameTagError("Two zipped values have not the same tag")
            res[j] = (kl(val1, val2) if tag1 is TAG_LEAF else kn(val1, val2), tag1)
        return res
    # </editor-fold>

    # <editor-fold desc="Reduce functions">
    def reduce_local(self: 'Segment[A, B]', k: Callable[[A, B, A], A],
                     phi: Callable[[B], C],
                     psi_l: Callable[[C, C, A], C],
                     psi_r: Callable[[A, C, C], C]
                     ) -> Tuple[Union[A, C], int]:
        assert not self.empty(), "reduce_local cannot be applied to an empty Segment"
        stack = []
        d = MINUS_INFINITY
        critic = False
        for (val, tag) in reversed(self):
            if tag is TAG_LEAF:
                stack.append(val)
                d = d + 1
            elif tag is TAG_NODE:
                if len(stack) < 2:
                    raise IllFormedError(
                        "reduce_local cannot be applied if there is a node that does not have"
                        "two children in the current instance")
                lv, rv = stack.pop(), stack.pop()
                if d == 0:
                    stack.append(psi_l(lv, phi(val), rv))
                elif d == 1:
                    stack.append(psi_r(lv, phi(val), rv))
                    d = 0
                else:
                    stack.append(k(lv, val, rv))
            else:
                stack.append(phi(val))
                critic = True
                d = 0
        top = stack.pop()
        return top, TAG_NODE if critic else TAG_LEAF

    def reduce_global(self: 'Segment[A, C]', psi_n: Callable[[A, C, A], A]):
        assert not self.has_critical(), "reduce_global cannot be applied to a Segments which contains a critical"
        assert not self.empty(), "reduce_global cannot be applied to an empty Segment"
        stack = []
        for (val, tag) in reversed(self):
            if tag is TAG_LEAF:
                stack.append(val)
            else:
                if len(stack) < 2:
                    raise IllFormedError(
                        "reduce_global cannot be applied if there is a node that does not have two children "
                        "in the current instance")
                lv, rv = stack.pop(), stack.pop()
                stack.append(psi_n(lv, val, rv))
        top = stack.pop()
        return top
    # </editor-fold>

    # <editor-fold desc="uAcc functions">
    def uacc_local(self: 'Segment[A, B]', k: Callable[[A, B, A], A],
                   phi: Callable[[B], C],
                   psi_l: Callable[[C, C, A], C],
                   psi_r: Callable[[A, C, C], C]
                   ) -> Tuple[Tuple[Union[A, C], int], 'Segment[A, Optional[A]]']:
        assert not self.empty(), "uacc_local cannot be applied to an empty Segment"
        stack = []
        d = MINUS_INFINITY
        lgth = self.length()
        res = Segment.init(lambda idx: None, lgth)
        critic = False
        for i in reversed(range(lgth)):
            (val, tag) = self[i]
            if tag is TAG_LEAF:
                res[i] = (val, tag)
                stack.append(val)
                d = d + 1
            elif tag is TAG_NODE:
                if len(stack) < 2:
                    raise IllFormedError(
                        "uacc_local cannot be applied if there is a node that does not have two children "
                        "in the current instance")
                lv, rv = stack.pop(), stack.pop()
                if d == 0:
                    stack.append(psi_l(lv, phi(val), rv))
                    res[i] = (None, tag)
                elif d == 1:
                    stack.append(psi_r(lv, phi(val), rv))
                    res[i] = (None, tag)
                    d = 0
                else:
                    new_val = k(lv, val, rv)
                    res[i] = (new_val, tag)
                    stack.append(new_val)
                    d = d - 1
            else:
                stack.append(phi(val))
                d = 0
                critic = True
                res[i] = (None, tag)
        top = stack.pop()
        return (top, TAG_NODE if critic else TAG_LEAF), res

    def uacc_global(self: 'Segment[A, C]', psi_n: Callable[[A, C, A], A]) -> 'Segment[A, A]':
        assert not self.has_critical(), "uacc_global cannot be applied to a Segments which contains a critical"
        stack = []
        lgth = self.length()
        res = Segment.init(lambda idx: None, lgth)
        for i in reversed(range(lgth)):
            (val, tag) = self[i]
            if tag is TAG_NODE:
                if len(stack) < 2:
                    raise IllFormedError(
                        "uacc_global cannot be applied if there is a node that does not have two children "
                        "in the current instance")
                lv, rv = stack.pop(), stack.pop()
                val = psi_n(lv, val, rv)
            res[i] = (val, tag)
            stack.append(val)
        return res

    def uacc_update(self: 'Segment[A, B]', seg2: 'Segment[A, Optional[A]]',
                    k: Callable[[A, B, A], A],
                    lc: A, rc: A) -> 'Segment[A, A]':
        lgth = self.length()
        assert lgth == seg2.length(), "uacc_update cannot needs to Segment of same size as input"
        stack = []
        d = MINUS_INFINITY
        res = Segment.init(lambda idx: None, lgth)
        for i in reversed(range(lgth)):
            val1, tag1 = self[i]
            val2, tag2 = seg2[i]
            if tag1 is TAG_LEAF:
                res[i] = (val2, tag2)
                stack.append(val2)
                d += 1
            elif tag1 is TAG_NODE:
                if len(stack) < 2:
                    raise IllFormedError(
                        "uacc_update cannot be applied if there is a node that does not have two children "
                        "in the current instance")
                lv, rv = stack.pop(), stack.pop()
                if d == 0 or d == 1:
                    val = k(lv, val1, rv)
                    res[i] = (val, tag1)
                    stack.append(val)
                    d = 0
                else:
                    res[i] = (val2, tag2)
                    stack.append(val2)
                    d -= 1
            else:
                lv = lc
                rv = rc
                val = k(lv, val1, rv)
                res[i] = (val, tag1)
                stack.append(val)
                d = 0
        return res

    # </editor-fold">

    # <editor-fold desc="dAcc functions">
    def dacc_path(self: 'Segment[A, B]',
                  phi_l: Callable[[B], D],
                  phi_r: Callable[[B], D],
                  psi_u: Callable[[D, D], D]) -> Tuple[Tuple[D, D], int]:
        assert not self.empty(), "dacc_path cannot be applied to an empty Segment"
        d = MINUS_INFINITY
        to_l, to_r = None, None
        critic = False
        for (val, tag) in reversed(self):
            if tag is TAG_LEAF:
                d = d + 1
            elif tag is TAG_NODE:
                if d == 0 or d == 1:
                    to_l = psi_u(phi_l(val), to_l)
                    to_r = psi_u(phi_l(val), to_r)
                    d = 0
                else:
                    d = d - 1
            else:
                critic = True
                to_l, to_r = phi_l(val), phi_r(val)
                d = 0
        if not critic:
            raise ApplicationError("dacc_path must be imperatively applied to a Segment which contains a critical node")
        return (to_l, to_r), TAG_NODE

    def dacc_global(self: 'Segment[Union[A, B], Tuple[D, D]]',
                    psi_d: Callable[[C, D], C], c: C) -> 'Segment[C, C]':
        assert not self.has_critical(), "dacc_global cannot be applied to Segment which contains a critical node"
        stack = [c]
        lgth = self.length()
        res = Segment.init(lambda idx: None, lgth)
        for i in range(lgth):
            (val, tag) = self[i]
            if len(stack) == 0:
                raise IllFormedError(
                    "dacc_global cannot be applied to ill-formed Segments that is two leaf values do not have a parent")
            new_val = stack.pop()
            res[i] = (new_val, tag)
            if tag is TAG_NODE:
                (to_l, to_r) = val
                stack.append(psi_d(new_val, to_r))
                stack.append(psi_d(new_val, to_l))
        return res

    def dacc_local(self: 'Segment[A, B]', gl, gr, c: C) -> 'Segment[C, C]':
        stack = [c]
        lgth = self.length()
        res = Segment.init(lambda idx: None, lgth)
        for i in range(lgth):
            (val, tag) = self[i]
            if len(stack) == 0:
                raise IllFormedError(
                    "dacc_local cannot be applied to a illformed segment")
            new_val = stack.pop()
            res[i] = (new_val, tag)
            if tag is TAG_NODE:
                stack.append(gr(new_val, val))
                stack.append(gl(new_val, val))
        return res
    # </editor-fold>


class LTree(__List, interface.BinTree, Generic[A, B]):
    # pylint: disable=too-many-public-methods
    """
    Linearized segment of tree.
    A list of pair (val, tag) of type union(A,B) * int

    Methods from abstract __List:
        init, length, empty

    Methods from interface BinTree:
        init_from_bt
        size, map, zip, map2,
        reduce, uacc, dacc

    Methods:
        deserialization
    """
    @staticmethod
    def init(value_at: Callable[[int], Any], size: int):
        assert size >= 0
        return LTree(Segment([value_at(i) for i in range(0, size)]))


    def __str__(self):
        res = "["
        for i in range(len(self)):
            res = res + str(self[i]) + (',' if i != len(self) - 1 else '')
        res = res + "]"
        return res


    def size(self: 'LTree[A, B]') -> int:
        res = 0
        for seg in self:
            res += len(seg)
        return res

    def map(self: 'LTree[A, B]', kl: Callable[[A], C], kn: Callable[[B], D]) -> 'LTree[C, D]':
        assert not self.empty(), "map cannot be applied to an empty linearized tree"
        lgth = self.length()
        res = LTree.init(lambda idx: None, lgth)
        for i in range(lgth):
            res[i] = self[i].map_local(kl, kn)
        return res

    def zip(self: 'LTree[A, B]',
            a_ltree: 'LTree[C, D]') -> 'LTree[Tuple[A, C], Tuple[B, D]]':
        lgth = self.length()
        assert lgth == a_ltree.length(), "The linearized trees have not the same shape"
        res = LTree.init(lambda idx: None, lgth)
        for i in range(lgth):
            res[i] = self[i].zip_local(a_ltree[i])
        return res

    def map2(self: 'LTree[A, B]', kl: Callable[[A, C], U], kn: Callable[[B, D], V],
             a_ltree: 'LTree[C, D]') -> 'LTree[U, V]':
        lgth = self.length()
        assert lgth == a_ltree.length(), "The linearized trees have not the same shape"
        res = LTree.init(lambda idx: None, lgth)
        for i in range(lgth):
            res[i] = self[i].map2_local(kl, kn, a_ltree[i])
        return res

    def reduce(self: 'LTree[A, B]', k: Callable[[A, B, A], A],
               phi: Callable[[B], C] = fun.idt,
               psi_n: Callable[[A, C, A], A] = None,
               psi_l: Callable[[C, C, A], C] = None,
               psi_r: Callable[[A, C, C], C] = None
               ) -> A:
        assert not self.empty(), "reduce cannot be applied to an empty linearized tree"
        lgth = self.length()
        tops = Segment.init(lambda idx: None, lgth)
        for i in range(lgth):
            tops[i] = self[i].reduce_local(k, phi, psi_l, psi_r)
        return tops.reduce_global(psi_n)

    def uacc(self: 'LTree[A, B]', k: Callable[[A, B, A], A],
             phi: Callable[[B], C] = fun.idt,
             psi_n: Callable[[A, C, A], A] = None,
             psi_l: Callable[[C, C, A], C] = None,
             psi_r: Callable[[A, C, C], C] = None
             ) -> 'LTree[A, A]':
        assert not self.empty(), "uacc cannot be applied to an empty linearized tree"
        lgth = self.length()
        gt = Segment.init(lambda idx: None, lgth)
        lt2 = LTree.init(lambda idx: None, lgth)
        for i in range(lgth):
            top, res = self[i].uacc_local(k, phi, psi_l, psi_r)
            gt[i] = top
            lt2[i] = res
        gt2 = gt.uacc_global(psi_n)
        res = LTree([None] * gt.length())
        for i in range(gt.length()):
            _, tag = gt[i]
            if tag is TAG_NODE:
                val_l, tag_l = gt2.get_left(i)
                val_r, tag_r = gt2.get_right(i)
                res[i] = self[i].uacc_update(lt2[i], k, val_l, val_r)
            else:
                res[i] = lt2[i]
        return res

    def dacc(self: 'LTree[A, B]', gl: Callable[[C, B], C], gr: Callable[[C, B], C], c: C,
             phi_l: Callable[[B], D] = fun.idt,
             phi_r: Callable[[B], D] = fun.idt,
             psi_u: Callable[[C, D], D] = None,
             psi_d: Callable[[C, D], C] = None
             ) -> 'BinTree [C, C]':
        assert not self.empty(), "dacc cannot be applied to an empty linearized tree"
        lgth = self.length()
        gt = Segment.init(lambda idx: None, lgth)
        res = LTree.init(lambda idx: None, lgth)
        for i in range(lgth):
            seg = self[i]
            if seg.has_critical():
                gt[i] = seg.dacc_path(phi_l, phi_r, psi_u)
            else:
                val, _ = seg[0]
                gt[i] = (val, TAG_LEAF)
        gt2 = gt.dacc_global(psi_d, c)
        for i in range(gt.length()):
            val_c, _ = gt2[i]
            res[i] = self[i].dacc_local(gl, gr, val_c)
        return res

    @staticmethod
    def init_from_bt(bt: 'BTree[A, B]', m: int = 1, ftag = Tag.mbridge) -> 'LTree[A, B]':
        def __tv2lv(bt_value):
            val, tag = bt_value.value
            res = Segment.init(fun.none, 0)
            res_0 = Segment.init(fun.none, 0)
            if tag is TAG_LEAF:
                res_0.append(bt_value.value)
                res.append(res_0)
            else:  # bt_val.is_node
                res_left = Segment(__tv2lv(bt_value.left))
                res_right = Segment(__tv2lv(bt_value.right))
                if tag is TAG_CRITICAL:
                    res_0.append(bt_value.value)
                    res.append(res_0)
                    res.extend(res_left)
                    res.extend(res_right)
                else:  # val.is_node
                    res_0.append((val, TAG_NODE))
                    res_0.extend(res_left[0])
                    res_0.extend(res_right[0])
                    res.append(res_0)
                    res.extend(res_left[1:])
                    res.extend(res_right[1:])
            return res
        bt_tagged = ftag(bt, m)
        return LTree(__tv2lv(bt_tagged))   

    def deserialization(self: 'LTree[A, B]') -> 'BTree[A, B]':
        def __lv2ibt(a_seg: 'Segment A B') -> Tuple[int, 'BTree[A, B]']:
            assert not a_seg.empty(), "An empty Segment cannot be transformed into a BTree"
            stack = []
            critical = False
            for idx in reversed(range(a_seg.length())):
                val_s, tag_s = a_seg[idx]
                if tag_s is TAG_LEAF:
                    stack.append(Leaf((val_s, tag_s)))
                elif tag_s is TAG_CRITICAL:
                    stack.append(Leaf((val_s, tag_s)))
                    if critical:
                        raise IllFormedError("A ill-formed Segment cannot be transformed into a BTree")
                    else:
                        critical = True
                else:
                    lv, rv = stack.pop(), stack.pop()
                    stack.append(Node((val_s, tag_s), lv, rv))
            if len(stack) is not 1:
                raise IllFormedError("A ill-formed Segment cannot be transformed into a BTree")
            else:
                return (TAG_NODE if critical else TAG_LEAF), stack[0]

        lgth = self.length()
        list_of_btree = SList.init(fun.none, lgth)
        gt = SList.init(fun.none, lgth)
        for i in range(lgth):
            seg = self[i]
            tag, bt_i = __lv2ibt(seg)
            gt[i] = tag
            list_of_btree[i] = bt_i

        def __rev_segment_to_trees(lb, glob):
            stack = []
            for i in reversed(range(lb.length())):
                if glob[i] is TAG_LEAF:
                    stack.append(lb[i])
                else:
                    lbt, rbt = stack.pop(), stack.pop()

                    def __graft(bt, lbt, rbt):
                        val = bt.value
                        if bt.is_node:
                            return Node(val, __graft(bt.left, lbt, rbt), __graft(bt.right, lbt, rbt))
                        else:  # bt.is_leaf()
                            return Node(val, lbt, rbt) if val[1] is TAG_CRITICAL else bt

                    stack.append(__graft(lb[i], lbt, rbt))
            if len(stack) != 1:
                raise IllFormedError("A ill-formed list of incomplete BTree cannot be transformed into a BTree")
            else:
                return stack[0]

        annoted_btree = __rev_segment_to_trees(list_of_btree, gt)
        return annoted_btree.map(lambda leaf: leaf[0], lambda node: node[0])
