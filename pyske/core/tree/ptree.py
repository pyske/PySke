from typing import Generic, TypeVar, Callable, Tuple

from pyske.core import interface, SList
from pyske.core.tree.distribution import Distribution
from pyske.core.tree.ltree import LTree, Segment
from pyske.core.tree.btree import BTree

from pyske.core.tree.tag import TAG_NODE, TAG_LEAF

from pyske.core.util import fun

from pyske.core.support import parallel

import itertools

__all__ = ['PTree']

# <editor-fold desc="constants">
A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
C = TypeVar('C')  # pylint: disable=invalid-name
D = TypeVar('D')  # pylint: disable=invalid-name
U = TypeVar('U')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name

TAG_BASE = "12367890"  # pylint: disable=invalid-name
TAG_COMM_REDUCE = int(TAG_BASE + "11")  # pylint: disable=invalid-name
TAG_COMM_UACC_1 = int(TAG_BASE + "21")  # pylint: disable=invalid-name
TAG_COMM_UACC_2 = int(TAG_BASE + "22")  # pylint: disable=invalid-name
TAG_COMM_DACC_1 = int(TAG_BASE + "31")  # pylint: disable=invalid-name
TAG_COMM_DACC_2 = int(TAG_BASE + "32")  # pylint: disable=invalid-name
TAG_COMM_MERGE = int(TAG_BASE + "00")  # pylint: disable=invalid-name
TAG_TO_SEQ = int(TAG_BASE + "01")  # pylint: disable=invalid-name

_PID: int = parallel.PID
_NPROCS: int = parallel.NPROCS
_COMM = parallel.COMM
# </editor-fold>


class PTree(interface.BinTree, Generic[A, B]):
    # pylint: disable=too-many-public-methods
    """
    PySke distributed binary trees

    Methods from interface BinTree:
        init_from_bt,
        size, map, zip, map2,
        reduce, uacc, dacc

    Methods:
        init_from_seq, to_seq
    """

    def __init__(self):
        self.__distribution = Distribution([0 for _ in range(_NPROCS)])
        self.__global_index = SList()
        self.__start_index = 0
        self.__nb_segs = 0
        self.__content = SList()
        self.__local_size = 0
        self.__global_size = 0
        self.__local_index = SList()

    def __str__(self):
        return "PID[" + str(_PID) + "]:\n" + \
               "  global_index: " + str(self.__global_index) + "\n" + \
               "  local_index: " + str(self.__local_index) + "\n" + \
               "  distribution: " + str(self.__distribution) + "\n" + \
               "  nb_segs: " + str(self.__nb_segs) + "\n" + \
               "  start_index: " + str(self.__start_index) + "\n" + \
               "  content: " + self.str_content(print_pid = False) + "\n" + \
               "  local_size: " + str(self.__local_size) + "\n" + \
               "  global_size: " + str(self.__global_size) + "\n"

    def str_content(self, print_pid = True):
        """Browse the linearized distributed tree contained in the current processor
        """
        res = "PID[" + str(_PID) + "]: [" if print_pid else ""
        for i in range(len(self.__local_index)):
            (start, offset) = self.__global_index[i]
            seg = Segment(self.__content[start:start + offset])
            res = res + str(seg)+ (',' if i != len(self.__local_index) - 1 else '')
        return res+"]"

    def __eq__(self, other):
        if isinstance(other, PTree):
            return self.__distribution == other.__distribution \
                   and self.__global_index == other.__global_index\
                   and self.__local_index == other.__local_index\
                   and self.__start_index == other.__start_index \
                   and self.__nb_segs == other.__nb_segs \
                   and self.__content == other.__content \
                   and self.__local_size == other.__local_size \
                   and self.__global_size == other.__global_size
        else:
            return False

    @staticmethod
    def init_from_bt(bt: 'BTree[A, B]', m: int = 1) -> 'PTree[A, B]':
        lt = LTree.init_from_bt(bt, m)
        return PTree.from_seq(lt)

    @staticmethod
    def from_seq(lt: 'LTree[A, B]') -> 'PTree[A, B]':
        p_tree = PTree()
        sizes = [len(lt[i]) for i in range(len(lt))]
        (distribution, global_index) = Distribution.balanced_tree(sizes)
        p_tree.__distribution = distribution
        p_tree.__global_index = SList(global_index)
        p_tree.__start_index = SList(distribution).scanl(lambda x, y: x + y, 0)[_PID]
        p_tree.__nb_segs = distribution[_PID]
        p_tree.__global_size = lt.size()
        p_tree.__local_size = 0
        for i_seg in range(p_tree.__start_index, p_tree.__start_index + p_tree.__nb_segs):
            p_tree.__content.extend(lt[i_seg])
            p_tree.__local_size += len(lt[i_seg])
        p_tree.__local_index = p_tree.__get_local_index()
        return p_tree

    @staticmethod
    def gather_gt(gt, root=0):
        res = None
        data = _COMM.gather(gt, root=root)
        if _PID is 0:
            prime_gt = Segment()
            for g in data: 
                prime_gt.extend(g)
            res = prime_gt
        return res

    @staticmethod
    def allgather_gt(gt):
        gt2 = _COMM.allgather(gt)
        res = gt2[0]
        for i_seg in range(1, len(gt2)):
            res.extend(gt2[i_seg])
        return res

    @staticmethod
    def scatter_gt(gt, distribution, root=0):
        start = 0
        if _PID is 0:
            gts = [None] * len(distribution)
            acc_gt_size = 0
            for i in range(len(distribution)):
                dist = distribution[i]
                gts[i] = Segment(gt[acc_gt_size : acc_gt_size + dist])
                acc_gt_size += dist
        else:
            gts = None
        return _COMM.scatter(gts, root=root)

    def __get_full_index(self):
        def f(x, y):
            (x1, y1) = x
            (x2, y2) = y
            return x1 + y1, y2
        return SList(self.__global_index.scanr(f))

    def __get_local_index(self: 'PTree[A, B]'):
        return self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]

    def to_seq(self):
        full_content = []
        full_index = self.__get_full_index()
        res = LTree.init(fun.none, full_index.length())
        full_content.extend(self.__content)
        content2 = _COMM.allgather(full_content)
        prime_content = content2[0]
        for i_seg in range(1, len(content2)):
            prime_content.extend(content2[i_seg])
        for i in range(full_index.length()):
            (start, offset) = full_index[i]
            res[i] = Segment(prime_content[start:start + offset])
        return res

    @staticmethod
    def init(pt, new_content):
        p = PTree()
        p.__distribution = pt.__distribution
        p.__global_index = pt.__global_index
        p.__start_index = pt.__start_index
        p.__nb_segs = pt.__nb_segs
        p.__local_size = pt.__local_size
        p.__global_size = pt.__global_size
        p.__local_index = pt.__local_index
        p.__content = new_content
        return p

    def size(self: 'PTree[A, B]') -> int:
        return self.__global_size

    def map(self: 'PTree[A, B]', kl: Callable[[A], C], kn: Callable[[B], D]) -> 'PTree[C, D]':
        if len(self.__content) == 0:
            return self
        new_content = SList.init(fun.none, self.__local_size)
        for (start, offset) in self.__local_index:
            new_content[start:start + offset] = Segment(self.__content[start:start + offset]).map_local(kl, kn)
        return PTree.init(self, new_content)

    def zip(self: 'PTree[A, B]',
            a_bintree: 'PTree[C, D]') -> 'PTree[Tuple[A, C], Tuple[B, D]]':
        assert self.__distribution == a_bintree.__distribution
        new_content = SList.init(fun.none, self.__content.length())
        for i in range(len(self.__local_index)):
            start, offset = self.__local_index[i]
            new_content[start:start + offset] = Segment(self.__content[start:start+offset]).\
                zip_local(Segment(a_bintree.__content[start:start+offset]))
        res = PTree.init(self, new_content)
        return res

    def map2(self: 'PTree[A, B]', kl: Callable[[A, C], U], kn: Callable[[B, D], V],
             a_bintree: 'PTree[C, D]') -> 'PTree[U, V]':
        assert self.__distribution == a_bintree.__distribution
        new_content = SList.init(fun.none, self.__content.length())
        for i in range(len(self.__local_index)):
            start, offset = self.__local_index[i]
            new_content[start:start + offset] = Segment(self.__content[start:start+offset]).\
                map2_local(kl, kn, Segment(a_bintree.__content[start:start+offset]))
        res = PTree.init(self, new_content)
        return res

    def reduce(self: 'PTree[A, B]', k: Callable[[A, B, A], A],
               phi: Callable[[B], C] = fun.idt,
               psi_n: Callable[[A, C, A], A] = None,
               psi_l: Callable[[C, C, A], C] = None,
               psi_r: Callable[[A, C, C], C] = None
               ) -> A:
        gt = Segment.init(fun.none, self.__nb_segs)
        i = 0
        for (start, offset) in self.__local_index:
            gt[i] = Segment(self.__content[start:start + offset]).reduce_local(k, phi, psi_l, psi_r)
            i += 1
        gt = PTree.allgather_gt(gt)
        return gt.reduce_global(psi_n) 

    def uacc(self: 'PTree[A, B]', k: Callable[[A, B, A], A],
             phi: Callable[[B], C] = fun.idt,
             psi_n: Callable[[A, C, A], A] = None,
             psi_l: Callable[[C, C, A], C] = None,
             psi_r: Callable[[A, C, C], C] = None
             ) -> 'PTree[A, A]':
        if len(self.__content) == 0:
            return self
        gt = Segment.init(fun.none, self.__nb_segs)
        lt2 = SList.init(fun.none, self.__nb_segs)

        # Step 1 : Local Upwards Accumulation
        i = 0
        for (start, offset) in self.__local_index:
            gt[i], lt2[i] = Segment(self.__content[start:start + offset]).uacc_local(k, phi, psi_l, psi_r)
            i += 1
        # Step 2 : Gather local Results
        gt = PTree.gather_gt(gt)

        # Step 3 : Global Upward Accumulation
        gt2 = None
        if _PID is 0:
            gt2 = gt.uacc_global(psi_n)
            for i in range(len(gt2)):
                _, tag = gt2[i]
                if tag is TAG_NODE:
                    val_left, _ = gt2.get_left(i)
                    val_right, _ = gt2.get_right(i)
                    gt2[i] = (val_left, val_right), TAG_NODE

        # Step 4 : Distributing Global Result
        gt2 = PTree.scatter_gt(gt2, self.__distribution)

        # Step 5 : Local Updates
        new_content = SList.init(fun.none, self.__content.length())
        for i in range(len(self.__local_index)):
            start, offset = self.__local_index[i]
            _, tag = gt2[i]
            if tag is TAG_NODE:
                (lc, rc), _ = gt2[i]
                val = Segment(self.__content[start:start + offset]).uacc_update(lt2[i], k, lc, rc)
            else:
                val = lt2[i]
            new_content[start:start + offset] = val
        return PTree.init(self, new_content)

    def dacc(self: 'PTree[A, B]', gl: Callable[[C, B], C], gr: Callable[[C, B], C], c: C,
             phi_l: Callable[[B], D] = fun.idt,
             phi_r: Callable[[B], D] = fun.idt,
             psi_u: Callable[[C, D], D] = None,
             psi_d: Callable[[C, D], C] = None
             ) -> 'PTree [C, C]':
        # Step 1 : Computing Local Intermediate Values
        gt = Segment.init(fun.none, self.__nb_segs)
        i = 0
        for (start, offset) in self.__local_index:
            seg = Segment(self.__content[start:start + offset])
            if seg.has_critical():
                gt[i] = seg.dacc_path(phi_l, phi_r, psi_u)
            else:
                val, _ = seg[0]
                gt[i] = (val, TAG_LEAF)
            i += 1
        
        # Step 2 : Gather Local Results
        gt = PTree.gather_gt(gt)

        # Step 3 : Global Downward Accumulation
        gt2 = gt.dacc_global(psi_d, c) if _PID == 0 else None

        # Step 4 : Distributing Global Result
        gt2 = PTree.scatter_gt(gt2, self.__distribution)

        # Step 5 : Local Downward Accumulation
        new_content = SList.init(fun.none, self.__content.length())
        for i in range(len(self.__local_index)):
            start, offset = self.__local_index[i]
            val, _ = gt2[i]
            new_content[start:start + offset] = Segment(self.__content[start:start + offset]).dacc_local(gl, gr, val)
        return PTree.init(self, new_content)