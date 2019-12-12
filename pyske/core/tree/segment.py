from typing import Generic, TypeVar, Callable, Union, Tuple, Optional, Any
from pyske.core.tree.tag import TAG_LEAF, TAG_NODE, TAG_CRITICAL
from pyske.core.support.constant import MINUS_INFINITY
from pyske.core.support.errors import IllFormedError, ApplicationError, NotSameTagError
from pyske.core.support.constant import RIGHT, LEFT


__all__ = ['Segment']

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name
D = TypeVar('D')  # pylint: disable=invalid-name
E = TypeVar('E')  # pylint: disable=invalid-name
U = TypeVar('U')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name


class Segment(Generic[A, B]):
    # pylint: disable=too-many-public-methods
    """
    Linearized segment of tree.
    A list of pair (val, tag) of type union(A,B) * int

    Methods from abstract __List:
        init, length, empty

    Methods:
        has_critical, get_left, get_right,
        map_local, zip_local, map2_local,
        map_reduce_local,
        reduce_local, reduce_global,
        uacc_local, uacc_global, uacc_update,
        dacc_path, dacc_global, dacc_local,
        getch_local, getch_update
    """

    def __init__(self, content=None):
        if content is None:
            content = []
        self.__content = content
        self.__length = len(content)

    def __eq__(self: 'Segment[A, B]', other: Any) -> bool:
        if isinstance(other, Segment):
            if self.length != other.length:
                return False
            for i in range(0, self.length):
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
        for i in range(self.length):
            res = res + __str_v(self[i]) + (',' if i != self.length - 1 else '')
        res = res + "]"
        return res

    def __getitem__(self, key):
        return self.__content[key]

    def __setitem__(self, key, value):
        self.__content[key] = value

    def extend(self, c):
        self.__content.extend(c)
        self.__length += c.length

    def empty(self) -> bool:
        return self.length == 0

    def append(self, item):
        self.__content.append(item)
        self.__length += 1

    @property
    def length(self) -> int:
        return self.__length

    @staticmethod
    def init(value_at: Callable[[int], Any], size: int):
        assert size >= 0
        return Segment([value_at(i) for i in range(0, size)])

    def has_critical(self: 'Segment[A, B]') -> bool:
        for (val, tag) in self.__content:
            if tag is TAG_CRITICAL:
                return True
        return False

    def get_left(self: 'Segment[A, B]', i: int) -> Union[A, B]:
        assert not self.has_critical(), "The left children of a value in a non-global Segment cannot be found"
        assert self[i][1] is not TAG_LEAF, "A leaf value doesn't have a left children"
        assert i < self.length - 1, "Cannot get the left children of a node in an ill-formed Segment"
        return self[i + 1]

    def get_right(self: 'Segment[A, B]', i: int) -> Union[A, B]:
        assert not self.has_critical(), "The right children of a value in a non-global Segment cannot be found"
        assert self[i][1] is not TAG_LEAF, "A leaf value doesn't have a right children"
        assert i < self.length - 2, "Cannot get the left children of a node in an ill-formed Segment"

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
        res = Segment.init(lambda idx: None, self.length)
        for i in range(self.length):
            (val, tag) = self[i]
            res[i] = kl(val) if tag is TAG_LEAF else kn(val), tag
        return res

    def zip_local(self: 'Segment[A, B]', seg: 'Segment[C, D]') -> 'Segment[Tuple[A, C], Tuple[B, D]]':
        assert self.length == seg.length, "The linearized trees have not the same shape"
        res = Segment.init(lambda idx: None, self.length)
        for j in range(self.length):
            (val1, tag1) = self[j]
            (val2, tag2) = seg[j]
            if tag1 != tag2:
                raise NotSameTagError("Two zipped values have not the same tag")
            res[j] = ((val1, val2), tag1)
        return res

    def map2_local(self: 'Segment[A, B]', kl: Callable[[A, C], U],
                   kn: Callable[[B, D], V], seg: 'Segment[C, D]') -> 'Segment[U, V]':
        assert self.length == seg.length, "The linearized trees have not the same shape"
        res = Segment.init(lambda idx: None, self.length)
        for j in range(self.length):
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
        for (val, tag) in reversed(self.__content):
            if tag is TAG_LEAF:
                stack.append(val)
                d = d + 1
            elif tag is TAG_NODE:
                if len(stack) < 2:
                    raise IllFormedError(
                        "reduce_local cannot be applied if there is a node that does not have"
                        "two children in the current instance")
                lv, rv = stack.pop(), stack.pop()
                if d is LEFT:
                    stack.append(psi_l(lv, phi(val), rv))
                elif d is RIGHT:
                    stack.append(psi_r(lv, phi(val), rv))
                    d = LEFT
                else:
                    stack.append(k(lv, val, rv))
            else:
                stack.append(phi(val))
                critic = True
                d = 0
        top = stack.pop()
        return top, TAG_NODE if critic else TAG_LEAF

    def map_reduce_local(self: 'Segment[A, B]',
                         kl: Callable[[A], C], kn: Callable[[B], D],
                         k: Callable[[C, D, C], C],
                         phi: Callable[[D], E] = None,
                         psi_l: Callable[[E, E, C], E] = None,
                         psi_r: Callable[[C, E, E], E] = None) -> Tuple[Union[C, E], int]:
        assert not self.empty(), "map_reduce_local cannot be applied to an empty Segment"
        stack = []
        d = MINUS_INFINITY
        critic = False
        for (val, tag) in reversed(self.__content):
            if tag is TAG_LEAF:
                stack.append(kl(val))
                d = d + 1
            elif tag is TAG_NODE:
                if len(stack) < 2:
                    raise IllFormedError(
                        "reduce_local cannot be applied if there is a node that does not have"
                        "two children in the current instance")
                lv, rv = stack.pop(), stack.pop()
                if d == 0:
                    stack.append(psi_l(lv, phi(kn(val)), rv))
                elif d == 1:
                    stack.append(psi_r(lv, phi(kn(val)), rv))
                    d = 0
                else:
                    stack.append(k(lv, kn(val), rv))
            else:
                stack.append(phi(kn(val)))
                critic = True
                d = 0
        top = stack.pop()
        return top, TAG_NODE if critic else TAG_LEAF

    def reduce_global(self: 'Segment[A, C]', psi_n: Callable[[A, C, A], A]):
        assert not self.has_critical(), "reduce_global cannot be applied to a Segments which contains a critical"
        assert not self.empty(), "reduce_global cannot be applied to an empty Segment"
        stack = []
        for (val, tag) in reversed(self.__content):
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
        res = Segment.init(lambda idx: None, self.length)
        critic = False
        for i in reversed(range(self.length)):
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
        res = Segment.init(lambda idx: None, self.length)
        for i in reversed(range(self.length)):
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
        assert self.length == seg2.length, "uacc_update cannot needs to Segment of same size as input"
        stack = []
        d = MINUS_INFINITY
        res = Segment.init(lambda idx: None, self.length)
        for i in reversed(range(self.length)):
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
        for (val, tag) in reversed(self.__content):
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
        res = Segment.init(lambda idx: None, self.length)
        for i in range(self.length):
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
        res = Segment.init(lambda idx: None, self.length)
        for i in range(self.length):
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

    # <editor-fold desc="getchl and getchr functions">
    def getch_local(self: 'Segment[A, A]', c: A, side: int) -> Tuple[Tuple[A, int], 'Segment[A, A]']:
        res = Segment.init(lambda idx: None, self.length)
        crit = False
        d = 1  # Left:0; Right:1; init: right
        stack = []
        for i in reversed(range(self.length)):
            (val, tag) = self[i]
            if tag is TAG_LEAF:
                res[i] = (c, tag)
            if tag is TAG_NODE:
                new_val = stack.pop()
                res[i] = (new_val, tag)
            if tag is TAG_CRITICAL:
                crit = True
                res[i] = (None, tag)
            if d == side or i == 0:
                stack.append(val)
            d = (d + 1) % 2
        top = (stack.pop(), TAG_NODE if crit else TAG_LEAF)
        return top, res

    def getch_update(self: 'Segment[A, A]', c: A) -> 'Segment[A, A]':
        res = Segment.init(lambda idx: None, self.length)
        for i in reversed(range(self.length)):
            (val, tag) = self[i]
            if tag is TAG_CRITICAL:
                res[i] = (c, tag)
            else:
                res[i] = self[i]
        return res
    # </editor-fold>
