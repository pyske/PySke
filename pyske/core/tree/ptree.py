"""
PTree module
"""
import logging

from pyske.core.tree.ltree import TaggedValue, Segment, LTree
from pyske.core.support.parallel import COMM, PID, NPROCS
from pyske.core.support.separate import distribute_tree
from pyske.core.list.slist import SList
from pyske.core.util import par

TAG_BASE = "270995"
TAG_COMM_REDUCE = int(TAG_BASE + "11")
TAG_COMM_UACC_1 = int(TAG_BASE + "21")
TAG_COMM_UACC_2 = int(TAG_BASE + "22")
TAG_COMM_DACC_1 = int(TAG_BASE + "31")
TAG_COMM_DACC_2 = int(TAG_BASE + "32")
TAG_COMM_MERGE = int(TAG_BASE + "00")
TAG_TO_SEQ = int(TAG_BASE + "01")

logging.basicConfig(filename='run_ptree.log', level=logging.DEBUG)
with open('run_ptree.log', 'w'):
    pass
logger = logging.getLogger('ptree')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class PTree:
    # pylint: disable=too-many-instance-attributes

    """A class used to represent a distributed tree

    Attributes
    ----------
    __distribution: PID -> nb of segments
    __global_index: num seg -> (start, offset)
    __start_index: index of first index for the current PID in global_index
    __nb_segs: nb of indexes for the current PID in global_index
    __content: concatenation of the segments contained in the current instance
    """

    def __init__(self, lt=None):
        self.__distribution = SList([])
        self.__global_index = SList([])
        self.__start_index = 0
        self.__nb_segs = 0
        self.__content = SList([])
        if lt is not None:
            (distribution, global_index) = distribute_tree(lt, NPROCS)
            self.__distribution = distribution
            self.__global_index = global_index
            self.__start_index = distribution.scanl(lambda x, y: x + y, 0)[PID]
            self.__nb_segs = distribution[PID]
            for i_seg in range(self.__start_index, self.__start_index + self.__nb_segs):
                self.__content.extend(lt[i_seg])

    @property
    def distribution(self):
        """Distribution getter"""
        return self.__distribution

    @property
    def global_index(self):
        """Global index getter"""
        return self.__global_index

    @property
    def start_index(self):
        """Start index getter"""
        return self.__start_index

    @property
    def nb_segs(self):
        """Nb segs getter"""
        return self.__nb_segs

    @property
    def content(self):
        """Content getter"""
        return self.__content

    @distribution.setter
    def distribution(self, value):
        """Distribution setter"""
        self.__distribution = value

    @global_index.setter
    def global_index(self, value):
        """Global index setter"""
        self.__global_index = value

    @start_index.setter
    def start_index(self, value):
        """Start index setter"""
        self.__start_index = value

    @nb_segs.setter
    def nb_segs(self, value):
        """Nb segs setter"""
        self.__nb_segs = value

    @content.setter
    def content(self, value):
        """Content setter"""
        self.__content = value

    def __eq__(self, other):
        if isinstance(other, PTree):
            return self.__distribution == other.distribution \
                   and self.__global_index == other.distribution \
                   and self.__start_index == other.start_index \
                   and self.__nb_segs == other.nb_segs \
                   and self.__content == other.content
        return False

    @staticmethod
    def init(pt, content):
        """Factory for distributed tree.

        Creates a PTree from a already existing one, but changing its content

        Parameters
        ----------
        pt : :obj:`PTree`
            A parallel tree that we want to copy the distribution
        content : :obj:`SList`
            The content of the resulting PTree
        """
        p = PTree()
        p.distribution = pt.distribution
        p.global_index = pt.global_index
        p.start_index = pt.start_index
        p.nb_segs = pt.nb_segs
        p.content = content
        return p

    @staticmethod
    def init_from_file(filename, parser=int):
        """Instantiate a distributed tree from a file

        Parameters
        ----------
        filename : str
            The name of the file that contains the PTree to instantiate
        parser : callable, optional
            A function that transforms a string into a specific type.
            By default, string to int
        """
        filename = filename + "." + str(PID)

        def __parser_couple(s):
            s = s.replace("(", "")
            s = s.replace(")", "")
            ss = s.split(",")
            return int(ss[0]), int(ss[1])

        p = PTree()
        content = SList([])
        with open(filename, "r") as f:
            count_line = 0
            for line in f:
                if line.strip()[0] == '#':
                    continue
                # __distribution: PID -> nb of segments
                # __global_index: num seg -> (start, offset)
                if count_line == 0:  # Get the distribution
                    p.distribution = SList.from_str(line)
                    p.start_index = p.distribution.scanl(lambda x, y: x + y, 0)[PID]
                    p.nb_segs = p.distribution[PID]
                elif count_line == 1:  # Get the global_index
                    p.global_index = SList.from_str(line, parser=__parser_couple)
                else:  # Get the content
                    content.extend(Segment.from_str(line, parser=parser))
                count_line = count_line + 1
        p.content = content
        return p

    def __str__(self):
        return "PID[" + str(PID) + "]:\n" + \
               "  global_index: " + str(self.__global_index) + "\n" + \
               "  distribution: " + str(self.__distribution) + "\n" + \
               "  nb_segs: " + str(self.__nb_segs) + "\n" + \
               "  start_index: " + str(self.__start_index) + "\n" + \
               "  content: " + str(self.__content) + "\n"

    def browse(self):
        """Browse the linearized distributed tree contained in the current processor
        """
        res = "PID[" + str(PID) + "] "
        for (start, offset) in \
                self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]:
            seg = Segment(self.__content[start:start + offset])
            res = res + "\n   " + str(seg)
        return res

    def map(self, kl, kn):
        """Map skeleton for distributed tree

        Parameters
        ----------
        kl : callable
            Function to apply to every leaf value of the current instance
        kn : callable
            Function to apply to every node value of the current instance
        """
        content = SList([None] * self.__content.length())
        logger.debug(
            '[START] PID[%s] map skeleton', PID)
        for (start, offset) in \
                self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]:
            logger.debug('[START] PID[%s] map_local from %s to %s', PID, start, start + offset)
            content[start:start + offset] = Segment(self.__content[start:start +
                                                    offset]).map_local(kl, kn)
            logger.debug('[END] PID[%s] map_local from %s to %s', PID, start, start + offset)
        res = PTree.init(self, content)
        logger.debug('[END] PID[%s] map skeleton', PID)
        return res

    # pylint: disable=too-many-arguments
    def reduce(self, k, phi, psi_n, psi_l, psi_r):
        """Reduce skeleton for distributed tree

        The parameters must respect these equalities (closure property):
        * k(l, b, r) = psi_n(l, phi(b), r)
        * psi_n(psi_n(value, l, y), b, r) = psi_n(value, psi_l(l,b,r), y)
        * psi_n(l, b, psi_n(value, r, y)) = psi_n(value, psi_r(l,b,r), y)

        Parameters
        ----------
        k : callable
            The function used to reduce a BTree into a single value
        phi : callable
            A function used to respect the closure property to allow partial computation
        psi_n : callable
            A function used to respect the closure property to make partial computation
        psi_l : callable
            A function used to respect the closure property to make partial computation on the left
        psi_r : callable
            A function used to respect the closure property to make partial computation on the right
        """
        logger.debug('[START] PID[%s] reduce skeleton', PID)
        # Step 1 : Local Reduction
        gt = Segment([None] * self.__nb_segs)
        i = 0
        for (start, offset) in \
                self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]:
            logger.debug('[START] PID[%s] reduce_local from %s to %s', PID, start, start + offset)
            gt[i] = Segment(self.__content[start:start + offset]).reduce_local(k, phi, psi_l, psi_r)
            logger.debug('[END] PID[%s] reduce_local from %s to %s', PID, start, start + offset)
            i = i + 1
        # Step 2 : Gather local Results
        self.__gather_local_result(gt, i, TAG_COMM_UACC_1)
        # Step 3 : Global Reduction
        par.at_root(lambda: logger.debug('[START] PID[%s] reduce_global', PID))
        res = gt.reduce_global(psi_n) if PID == 0 else None
        par.at_root(lambda: logger.debug('[END] PID[%s] reduce_global', PID))
        logger.debug('[END] PID[%s] reduce skeleton', PID)
        return res

    def __local_upwards_accumulation(self, k, phi, psi_l, psi_r):
        gt = Segment([None] * self.__nb_segs)
        lt2 = SList([None] * self.__nb_segs)
        i = 0
        for (start, offset) in \
                self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]:
            logger.debug('[START] PID[%s] uacc_local from %s to %s', PID, start, start + offset)
            (top, res) = Segment(self.__content[start:start +
                                                offset]).uacc_local(k, phi, psi_l, psi_r)
            logger.debug('[END] PID[%s] uacc_local from %s to %s', PID, start, start + offset)
            gt[i] = top
            lt2[i] = res
            i = i + 1
        return i, gt, lt2

    @staticmethod
    def __gather_local_result(gt, i, tag):
        if PID == 0:
            for iproc in range(1, NPROCS):
                logger.debug('[START] PID[%s] reception local from %s', PID, i)
                gt.extend(COMM.recv(source=iproc, tag=tag)['c'])
                logger.debug('[END] PID[%s] reception local from %s', PID, i)
        else:
            logger.debug('[START] PID[%s] emission local to %s', PID, 0)
            COMM.send({'c': gt}, dest=0, tag=tag)
            logger.debug('[END] PID[%s] emission local to %s', PID, 0)

    @staticmethod
    def __global_upwards_accumulation(psi_n, gt):
        gt2 = None
        if PID == 0:
            par.at_root(lambda: logger.debug('[START] PID[%s] uacc_global', PID))
            gt2 = gt.uacc_global(psi_n)
            for i, _ in enumerate(gt2):
                if gt2[i].is_node():
                    gt2[i] = TaggedValue((gt2.get_left(i).get_value(),
                                          gt2.get_right(i).get_value()), gt2[i].get_tag())
            par.at_root(lambda: logger.debug('[END] PID[%s] uacc_global', PID))
        return gt2

    def __distribute_global_result(self, gt2, tag):
        start = 0
        if PID == 0:
            for iproc in range(NPROCS):
                iproc_off = self.__distribution[iproc]
                if iproc != 0:
                    logger.debug('[START] PID[%s] emission global to %s', PID, iproc)
                    COMM.send({'g': gt2[start: start + iproc_off]}, dest=iproc, tag=tag)
                    logger.debug('[END] PID[%s] emission global to %s', PID, iproc)
                start = start + iproc_off
        else:
            logger.debug('[START] PID[%s] reception global from %s', PID, 0)
            gt2 = COMM.recv(source=0, tag=tag)['g']
            logger.debug('[END] PID[%s] reception global from %s', PID, 0)
        return gt2

    def __local_updates(self, gt, gt2, lt2, k):
        content = SList([None] * self.__content.length())
        for i in range(len(self.__global_index[self.__start_index: self.__start_index +
                                               self.__nb_segs])):
            (start, offset) = self.__global_index[self.__start_index: self.__start_index +
                                                  self.__nb_segs][i]
            logger.debug('[START] PID[%s] uacc_update from %s to %s', PID, start, start + offset)
            if gt[i].is_node():
                (lc, rc) = gt2[i].get_value()
                val = Segment(self.__content[start:start + offset]).uacc_update(lt2[i], k, lc, rc)
            else:
                val = lt2[i]
            logger.debug('[END] PID[%s] uacc_update from %s to %s', PID, start, start + offset)
            content[start:start + offset] = val
        return content

    def uacc(self, k, phi, psi_n, psi_l, psi_r):
        """Upward accumulation skeleton for distributed tree

        The parameters must respect these equalities (closure property):
        * k(l, b, r) = psi_n(l, phi(b), r)
        * psi_n(psi_n(value, l, y), b, r) = psi_n(value, psi_l(l,b,r), y)
        * psi_n(l, b, psi_n(value, r, y)) = psi_n(value, psi_r(l,b,r), y)

        Parameters
        ----------
        k : callable
            The function used to reduce a BTree into a single value
        phi : callable
            A function used to respect the closure property to allow partial computation
        psi_n : callable
            A function used to respect the closure property to make partial computation
        psi_l : callable
            A function used to respect the closure property to make partial computation on the left
        psi_r : callable
            A function used to respect the closure property to make partial computation on the right
        """
        logger.debug('[START] PID[%s] uAcc skeleton', PID)
        assert self.__distribution != []
        # Step 1 : Local Upwards Accumulation
        i, gt, lt2 = self.__local_upwards_accumulation(k, phi, psi_l, psi_r)

        # Step 2 : Gather local Results
        self.__gather_local_result(gt, i, TAG_COMM_UACC_1)

        # Step 3 : Global Upward Accumulation
        gt2 = self.__global_upwards_accumulation(psi_n, gt)

        # Step 4 : Distributing Global Result
        gt2 = self.__distribute_global_result(gt2, TAG_COMM_UACC_2)

        # Step 5 : Local Updates
        content = self.__local_updates(gt, gt2, lt2, k)

        res = PTree.init(self, content)
        logger.debug('[END] PID[%s] uAcc skeleton', PID)
        return res

    def dacc(self, gl, gr, c, phi_l, phi_r, psi_u, psi_d):
        """Downward accumulation skeleton for distributed tree

        The parameters must respect these equalities (closure property):
        * gl(c, b) = psi_d(c, phi_l(b))
        * gr(c, b) = psi_d(c, phi_r(b))
        * psi_d(psi_d(c, b), a) = psi_d(c, psi_u(b,a))

        Parameters
        ---------
        gl : callable
            The function used to make an accumulation to the left children in a binary tree
        gr : callable
            The function used to make an accumulation to the right children in a binary tree
        c
            Initial value of accumulation
        phi_l : callable
            A function used to respect the closure property to allow partial computation on the left
        phi_r : callable
            A function used to respect the closure property to allow partial computation on the right
        psi_d : callable
            A function used to respect the closure property to make partial downward accumulation
        psi_u : callable
            A function used to respect the closure property to make partial computation
        """
        logger.debug('[START] PID[%s] dAcc skeleton', PID)
        # Step 1 : Computing Local Intermediate Values
        gt = Segment([None] * self.__nb_segs)
        i = 0
        for (start, offset) in \
                self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]:
            seg = Segment(self.__content[start:start + offset])
            logger.debug('[START] PID[%s] dacc_path from %s to %s', PID, start, start + offset)
            if seg.has_critical():
                gt[i] = seg.dacc_path(phi_l, phi_r, psi_u)
            else:
                gt[i] = TaggedValue(seg[0].get_value(), "L")
            logger.debug('[END] PID[%s] dacc_path from %s to %s', PID, start, start + offset)
            i = i + 1
        # Step 2 : Gather Local Results
        self.__gather_local_result(gt, i, TAG_COMM_DACC_1)
        # Step 3 : Global Downward Accumulation
        par.at_root(lambda: logger.debug('[START] PID[%s] dacc_global', PID))
        gt2 = (gt.dacc_global(psi_d, c) if PID == 0 else None)
        par.at_root(lambda: logger.debug('[END] PID[%s] dacc_global', PID))
        # Step 4 : Distributing Global Result
        gt2 = self.__distribute_global_result(gt2, TAG_COMM_DACC_2)
        # Step 5 : Local Downward Accumulation
        content = SList([None] * self.__content.length())
        for i in range(len(self.__global_index[self.__start_index: self.__start_index +
                                               self.__nb_segs])):
            (start, offset) = self.__global_index[self.__start_index: self.__start_index +
                                                  self.__nb_segs][i]
            logger.debug('[START] PID[%s] dacc_local from %s to %s', PID, start, start + offset)
            content[start:start + offset] = \
                Segment(self.__content[start:start + offset]).dacc_local(gl, gr, gt2[i].get_value())
            logger.debug('[END] PID[%s] dacc_local from %s to %s', PID, start, start + offset)
        logger.debug('[END] PID[%s] dAcc skeleton', PID)
        return PTree.init(self, content)

    def zip(self, pt: 'PTree'):
        """Zip skeleton for distributed tree

        Precondition
        -------------
        The distributions of self and pt should be the same

        Parameters
        ----------
        pt : :obj:`PTree`
            The PTree to zip with the current instance
        """
        logger.debug('[START] PID[%s] zip skeleton', PID)
        assert self.__distribution == pt.distribution
        content = SList([None] * self.__content.length())
        for i in range(len(self.__global_index[self.__start_index: self.__start_index +
                                               self.__nb_segs])):
            (start, offset) = self.__global_index[self.__start_index: self.__start_index +
                                                  self.__nb_segs][i]
            logger.debug('[START] PID[%s] zip_local from %s to %s', PID, start, start + offset)
            content[start:start + offset] = Segment(self.__content[start:start + offset]). \
                zip(Segment(pt.content[start:start + offset]))
            logger.debug('[END] PID[%s] zip_local from %s to %s', PID, start, start + offset)
        res = PTree.init(self, content)
        logger.debug('[END] PID[%s] zip skeleton', PID)
        return res

    def map2(self, f, pt):
        """Map2 skeleton for distributed tree

        Precondition
        -------------
        The distributions of self and pt should be the same

        Parameters
        ----------
        pt : :obj:`LTree`
            The LTree to zip with the current instance
        f : callable
            A function to zip values
        """
        logger.debug('[START] PID[%s] map2 skeleton', PID)
        assert self.__distribution == pt.distribution
        content = SList([None] * self.__content.length())
        for i in range(len(self.__global_index[self.__start_index: self.__start_index +
                                               self.__nb_segs])):
            (start, offset) = self.__global_index[self.__start_index: self.__start_index +
                                                  self.__nb_segs][i]
            logger.debug('[START] PID[%s] map2_local from %s to %s', PID, start, start + offset)
            content[start:start + offset] = Segment(self.__content[start:start + offset]). \
                map2(f, Segment(pt.content[start:start + offset]))
            logger.debug('[END] PID[%s] map2_local from %s to %s', PID, start, start + offset)
        res = PTree.init(self, content)
        logger.debug('[END] PID[%s] map2 skeleton', PID)
        return res

    def get_full_index(self):
        def f(x, y):
            (x1, y1) = x
            (_, y2) = y
            return x1 + y1, y2

        return SList(self.__global_index.scanr(f))

    def to_seq(self):
        full_content = []
        if PID == 0:
            full_index = self.get_full_index()
            res = LTree([None] * full_index.length())
            full_content.extend(self.__content)
            for iproc in range(1, NPROCS):
                full_content.extend(COMM.recv(source=iproc, tag=TAG_TO_SEQ)['c'])

            for i in range(full_index.length()):
                (start, offset) = full_index[i]
                res[i] = full_content[start:start + offset]
            return res
        COMM.send({'c': self.__content}, dest=0, tag=TAG_TO_SEQ)
        return None
