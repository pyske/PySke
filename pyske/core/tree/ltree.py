from pyske.core import interface, SList
from pyske.core.support.constant import LEFT
from pyske.core.util import fun
from pyske.core.support import constant
from pyske.core.tree.btree import BTree, Node, Leaf
from pyske.core.tree.tag import Tag, TAG_LEAF, TAG_NODE, TAG_CRITICAL
from pyske.core.tree.segment import Segment
from pyske.core.support.errors import IllFormedError

from typing import Generic, TypeVar, Callable, Tuple, Any, Optional

__all__ = ['LTree']

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
A1 = TypeVar('A1')  # pylint: disable=invalid-name
B1 = TypeVar('B1')  # pylint: disable=invalid-name
A2 = TypeVar('A2')  # pylint: disable=invalid-name
B2 = TypeVar('B2')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name
D = TypeVar('D')  # pylint: disable=invalid-name
E = TypeVar('E')  # pylint: disable=invalid-name
U = TypeVar('U')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name


class LTree(interface.BinTree, Generic[A, B]):
    # pylint: disable=too-many-public-methods
    """
    Linearized segment of tree.
    A list of pair (val, tag) of type union(A,B) * int

    Static method:
        init

    Methods from interface BinTree:
        from_bt, to_bt,
        length, empty
        size, map, zip, map2,
        reduce, uacc, dacc,
        getchl, getchr

    Methods:
        deserialization
    """
    def __init__(self, content=None):
        if content is None:
            content = []
        if isinstance(content, Segment):
            content = [content]
        self.__content = content
        self.__length = len(content)

    def __str__(self):
        res = "["
        for i in range(self.__length):
            res = res + str(self[i]) + (',' if i != self.__length - 1 else '')
        res = res + "]"
        return res

    def __eq__(self: 'LTree[A, B]', other: Any) -> bool:
        if isinstance(other, LTree):
            if self.length != other.length:
                return False
            for i in range(0, self.length):
                if self[i] != other[i]:
                    return False
            return True
        return False

    @property
    def length(self) -> int:
        return self.__length

    def empty(self) -> bool:
        return self.__content == []

    def extend(self, c):
        self.__content.extend(c)
        self.__length += c.length

    def append(self, item):
        self.__content.append(item)
        self.__length += 1

    def __getitem__(self, key):
        return self.__content[key]

    def __setitem__(self, key, value):
        self.__content[key] = value

    @staticmethod
    def init(value_at: Callable[[int], Any], size: int):
        assert size >= 0
        return LTree([value_at(i) for i in range(0, size)])

    @staticmethod
    def from_bt(bt: 'BTree[A, B]', m: int = 1, ftag=Tag.mbridge) -> 'LTree[A, B]':

        def __tv2lv(bt_value):
            val, tag = bt_value.value
            res = LTree.init(fun.none, 0)
            current_seg = Segment.init(fun.none, 0)
            if tag is TAG_LEAF:
                current_seg.append(bt_value.value)
                res.append(current_seg)
            else:  # bt_val.is_node
                res_left = __tv2lv(bt_value.left)
                res_right = __tv2lv(bt_value.right)
                if tag is TAG_CRITICAL:
                    current_seg.append(bt_value.value)
                    res.append(current_seg)
                    res.extend(res_left)
                    res.extend(res_right)
                else:  # val.is_node
                    current_seg.append(bt_value.value)
                    current_seg.extend(res_left[0])
                    current_seg.extend(res_right[0])
                    res.append(current_seg)
                    res.extend(LTree(res_left[1:]))
                    res.extend(LTree(res_right[1:]))
                    # res.extend(res_right[1:])
                    # res.extend(res_right[1:])
            return res

        # res = LTree.init(fun.none, 0)
        #

        bt_tagged = ftag(bt, m)
        segs = __tv2lv(bt_tagged)
        # return LTree(segs)
        return segs

    def to_bt(self: 'LTree[A, B]') -> 'BTree[A, B]':
        def __lv2ibt(a_seg: 'Segment A B') -> Tuple[int, 'BTree[A, B]']:
            assert not a_seg.empty(), "An empty Segment cannot be transformed into a BTree"
            stack = []
            critical = False
            for idx in reversed(range(a_seg.length)):
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

        list_of_btree = SList.init(fun.none, self.length)
        gt = SList.init(fun.none, self.length)
        for i in range(self.length):
            seg = self[i]
            tag, bt_i = __lv2ibt(seg)
            gt[i] = tag
            list_of_btree[i] = bt_i

        def __rev_segment_to_trees(lb, glob):
            stack = []
            for j in reversed(range(lb.length())):
                if glob[j] is TAG_LEAF:
                    stack.append(lb[j])
                else:
                    lbt, rbt = stack.pop(), stack.pop()

                    def __graft(bt, left_bt, right_bt):
                        val = bt.value
                        if bt.is_node:
                            return Node(val, __graft(bt.left, left_bt, right_bt), __graft(bt.right, left_bt, right_bt))
                        else:  # bt.is_leaf()
                            return Node(val, left_bt, right_bt) if val[1] is TAG_CRITICAL else bt

                    stack.append(__graft(lb[j], lbt, rbt))
            if len(stack) != 1:
                raise IllFormedError("A ill-formed list of incomplete BTree cannot be transformed into a BTree")
            else:
                return stack[0]

        annoted_btree = __rev_segment_to_trees(list_of_btree, gt)

        return annoted_btree.map(lambda leaf: leaf[0], lambda node: node[0])

    def size(self: 'LTree[A, B]') -> int:
        res = 0
        for seg in self.__content:
            res += seg.length
        return res

    def map(self: 'LTree[A, B]', kl: Callable[[A], C], kn: Callable[[B], D]) -> 'LTree[C, D]':
        assert not self.empty(), "map cannot be applied to an empty linearized tree"
        res = LTree.init(lambda idx: None, self.length)
        for i in range(self.length):
            res[i] = self[i].map_local(kl, kn)
        return res

    def zip(self: 'LTree[A, B]',
            a_ltree: 'LTree[C, D]') -> 'LTree[Tuple[A, C], Tuple[B, D]]':
        assert self.length == a_ltree.length, "The linearized trees have not the same shape"
        res = LTree.init(lambda idx: None, self.length)
        for i in range(self.length):
            res[i] = self[i].zip_local(a_ltree[i])
        return res

    def map2(self: 'LTree[A, B]', kl: Callable[[A, C], U], kn: Callable[[B, D], V],
             a_ltree: 'LTree[C, D]') -> 'LTree[U, V]':
        assert self.length == a_ltree.length, "The linearized trees have not the same shape"
        res = LTree.init(lambda idx: None, self.length)
        for i in range(self.length):
            res[i] = self[i].map2_local(kl, kn, a_ltree[i])
        return res

    def reduce(self: 'LTree[A, B]', k: Callable[[A, B, A], A],
               phi: Callable[[B], C] = fun.idt,
               psi_n: Callable[[A, C, A], A] = None,
               psi_l: Callable[[C, C, A], C] = None,
               psi_r: Callable[[A, C, C], C] = None
               ) -> A:
        assert not self.empty(), "reduce cannot be applied to an empty linearized tree"
        tops = Segment.init(lambda idx: None, self.length)
        for i in range(self.length):
            tops[i] = self[i].reduce_local(k, phi, psi_l, psi_r)
        return tops.reduce_global(psi_n)

    def map_reduce(self: 'LTree[A, B]', kl: Callable[[A], C], kn: Callable[[B], D],
                   k: Callable[[C, D, C], C],
                   phi: Callable[[D], E] = None,
                   psi_n: Callable[[C, E, C], C] = None,
                   psi_l: Callable[[E, E, C], E] = None,
                   psi_r: Callable[[C, E, E], E] = None
                   ):
        assert not self.empty(), "map_reduce cannot be applied to an empty linearized tree"
        tops = Segment.init(lambda idx: None, self.length)
        for i in range(self.length):
            tops[i] = self[i].map_reduce_local(kl, kn, k, phi, psi_l, psi_r)
        return tops.reduce_global(psi_n)

    def zip_reduce(self: 'LTree[A, B]', a_ltree: 'LTree[C, D]',
                   k: Callable[[Tuple[A, C], Tuple[B, D], Tuple[A, C]], Tuple[A, C]],
                   phi: Callable[[Tuple[B, D]], D] = None,
                   psi_n: Callable[[Tuple[A, C], D, Tuple[A , C]], Tuple[A, C]] = None,
                   psi_l: Callable[[D, D, Tuple[A, C]], D] = None,
                   psi_r: Callable[[Tuple[A, C], D, D], D] = None) -> Tuple[A, C]:
        assert not (self.empty() or a_ltree.empty()), "zip_reduce cannot be applied to an empty linearized tree"
        assert self.length == a_ltree.length, "The linearized trees have not the same shape"
        tops = Segment.init(lambda idx: None, self.length)
        for i in range(self.length):
            tops[i] = self[i].zip_reduce_local(a_ltree[i], k, phi, psi_l, psi_r)
        return tops.reduce_global(psi_n)

    def map2_reduce(self: 'BTree[A1, B1]',
                    kl: Callable[[A1, A2], A], kn: Callable[[B1, B2], B],
                    a_ltree: 'BTree[A2, B2]', k: Callable[[A, B, A], A],
                    phi: Callable[[B], C] = None, psi_n: Callable[[A, C, A], A] = None,
                    psi_l: Callable[[C, C, A], C] = None, psi_r: Callable[[A, C, C], C] = None
                    ) -> A:
        assert not (self.empty() or a_ltree.empty()), "zip_reduce cannot be applied to an empty linearized tree"
        assert self.length == a_ltree.length, "The linearized trees have not the same shape"
        tops = Segment.init(lambda idx: None, self.length)
        for i in range(self.length):
            tops[i] = self[i].map2_reduce_local(kl, kn, a_ltree[i], k, phi, psi_l, psi_r)
        return tops.reduce_global(psi_n)

    def uacc(self: 'LTree[A, B]', k: Callable[[A, B, A], A],
             phi: Callable[[B], C] = fun.idt,
             psi_n: Callable[[A, C, A], A] = None,
             psi_l: Callable[[C, C, A], C] = None,
             psi_r: Callable[[A, C, C], C] = None
             ) -> 'LTree[A, A]':
        assert not self.empty(), "uacc cannot be applied to an empty linearized tree"
        gt = Segment.init(lambda idx: None, self.length)
        lt2 = LTree.init(lambda idx: None, self.length)
        for i in range(self.length):
            top, res = self[i].uacc_local(k, phi, psi_l, psi_r)
            gt[i] = top
            lt2[i] = res
        gt2 = gt.uacc_global(psi_n)
        res = LTree([None] * gt.length)
        for i in range(gt.length):
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
        gt = Segment.init(lambda idx: None, self.length)
        res = LTree.init(lambda idx: None, self.length)
        for i in range(self.length):
            seg = self[i]
            if seg.has_critical():
                gt[i] = seg.dacc_path(phi_l, phi_r, psi_u)
            else:
                val, _ = seg[0]
                gt[i] = (val, TAG_LEAF)
        gt2 = gt.dacc_global(psi_d, c)
        for i in range(gt.length):
            val_c, _ = gt2[i]
            res[i] = self[i].dacc_local(gl, gr, val_c)
        return res

    def getchl(self: 'LTree[A, A]', c: A) -> 'LTree[A, A]':
        assert not self.empty(), "getchl cannot be applied to an empty linearized tree"
        gt = Segment.init(lambda idx: None, self.length)
        lt2 = LTree([None] * self.length)
        res = LTree([None] * self.length)
        for i in range(self.length):
            gt[i], lt2[i] = self[i].getch_local(c, side=constant.LEFT)
        for i in range(gt.length):
            _, tag = gt[i]
            if tag is TAG_NODE:
                val_l, _ = gt.get_left(i)
                res[i] = lt2[i].getch_update(val_l)
            else:
                res[i] = lt2[i]
        return res

    def getchr(self: 'LTree[A, A]', c: A) -> 'LTree[A, A]':
        assert not self.empty(), "getchr cannot be applied to an empty linearized tree"
        gt = Segment.init(lambda idx: None, self.length)
        lt2 = LTree([None] * self.length)
        res = LTree([None] * self.length)
        for i in range(self.length):
            gt[i], lt2[i] = self[i].getch_local(c, side=constant.RIGHT)
        for i in range(gt.length()):
            _, tag = gt[i]
            if tag is TAG_NODE:
                val_l, _ = gt.get_right(i)
                res[i] = lt2[i].getch_update(val_l)
            else:
                res[i] = lt2[i]
        return res

    def get_one_node(self: 'LTree[A, B]', p: Callable[[B], bool]) -> Optional[B]:
        for s in self.__content:
            r = s.get_first_node(p)
            if r is not None:
                return r
        return None

    def get_all_nodes(self: 'LTree[A, B]', p: Callable[[B], bool]) -> SList[B]:
        res = SList()
        for s in self.__content:
            for r in s.get_all_nodes(p):
                res.append(r)
        return res

    def get_one_leaf(self: 'LTree[A, B]', p: Callable[[A], bool], strategy=LEFT) -> Optional[A]:
        for s in self.__content if strategy is LEFT else reversed(self.__content):
            r = s.get_first_leaf(p, strategy)
            if r is not None:
                return r
        return None

    def get_all_leaves(self: 'LTree[A, B]', p: Callable[[A], bool], strategy=LEFT) -> SList[A]:
        res = SList()
        for s in self.__content if strategy is LEFT else reversed(self.__content):
            for r in s.get_all_leaves(p, strategy):
                res.append(r)
        return res

    def get_one(self: 'LTree[A, A]', p: Callable[[A], bool]) -> Optional[A]:
        for s in self.__content:
            r = s.get_first(p)
            if r is not None:
                return r
        return None

    def get_all(self: 'LTree[A, A]', p: Callable[[A], bool]) -> SList[A]:
        res = SList()
        for s in self.__content:
            for r in s.get_all(p):
                res.append(r)
        return res
