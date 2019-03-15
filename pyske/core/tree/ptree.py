from pyske.core.tree.ltree import TaggedValue, Segment, LTree
from pyske.core.support.parallel import *
from pyske.core.support.separate import *


TAG_BASE = "270995"
TAG_COMM_REDUCE = int(TAG_BASE + "11")
TAG_COMM_UACC_1 = int(TAG_BASE + "21")
TAG_COMM_UACC_2 = int(TAG_BASE + "22")
TAG_COMM_DACC_1 = int(TAG_BASE + "31")
TAG_COMM_DACC_2 = int(TAG_BASE + "32")
TAG_COMM_MERGE = int(TAG_BASE + "00")
TAG_TO_SEQ = int(TAG_BASE + "01")


class PTree:
    """A class used to represent a distributed tree

    Attributes
    ----------
    __distribution: pid -> nb of segments
    __global_index: num seg -> (start, offset)
    __start_index: index of first index for the current pid in global_index
    __nb_segs: nb of indexes for the current pid in global_index
    __content: concatenation of the segments contained in the current instance
    """

    def __init__(self, lt=None):
        self.__distribution = SList([])
        self.__global_index = SList([])
        self.__start_index = 0
        self.__nb_segs = 0
        self.__content = SList([])
        if lt is not None:
            (distribution, global_index) = distribute_tree(lt, nprocs)
            self.__distribution = distribution
            self.__global_index = global_index
            self.__start_index = distribution.scanl(lambda x, y: x + y, 0)[pid]
            self.__nb_segs = distribution[pid]
            for i_seg in range(self.__start_index, self.__start_index + self.__nb_segs):
                self.__content.extend(lt[i_seg])

    def __eq__(self, other):
        if isinstance(other, PTree):
            return self.__distribution == other.__distribution \
                   and self.__global_index == other.__distribution \
                   and self.__start_index == other.__start_index \
                   and self.__nb_segs == other.__nb_segs \
                   and self.__content == other.__content
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
        p.__distribution = pt.__distribution
        p.__global_index = pt.__global_index
        p.__start_index = pt.__start_index
        p.__nb_segs = pt.__nb_segs
        p.__content = content
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
        filename = filename + "." + str(pid)

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
                # __distribution: pid -> nb of segments
                # __global_index: num seg -> (start, offset)
                if count_line == 0:  # Get the distribution
                    p.__distribution = SList.from_str(line)
                    p.__start_index = p.__distribution.scanl(lambda x, y: x + y, 0)[pid]
                    p.__nb_segs = p.__distribution[pid]
                elif count_line == 1:  # Get the global_index
                    p.__global_index = SList.from_str(line, parser=__parser_couple)
                else:  # Get the content
                    content.extend(Segment.from_str(line, parser=parser))
                count_line = count_line + 1
        p.__content = content
        return p

    def __str__(self):
        return "pid[" + str(pid) + "]:\n" + \
               "  global_index: " + str(self.__global_index) + "\n" + \
               "  distribution: " + str(self.__distribution) + "\n" + \
               "  nb_segs: " + str(self.__nb_segs) + "\n" + \
               "  start_index: " + str(self.__start_index) + "\n" + \
               "  content: " + str(self.__content) + "\n"

    def browse(self):
        """Browse the linearized distributed tree contained in the current processor
        """
        res = "pid[" + str(pid) + "] "
        for (start, offset) in self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]:
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
        content = SList()
        for (start, offset) in self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]:
            content.extend(Segment(self.__content[start:start + offset]).map_local(kl, kn))
        return PTree.init(self, content)

    def reduce(self, k, phi, psi_n, psi_l, psi_r):
        """Reduce skeleton for distributed tree

        The parameters must respect these equalities (closure property):
        * k(l, b, r) = psi_n(l, phi(b), r)
        * psi_n(psi_n(x, l, y), b, r) = psi_n(x, psi_l(l,b,r), y)
        * psi_n(l, b, psi_n(x, r, y)) = psi_n(x, psi_r(l,b,r), y)

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
        # Step 1 : Local Reduction
        gt = Segment([None] * self.__nb_segs)
        i = 0
        for (start, offset) in self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]:
            gt[i] = Segment(self.__content[start:start + offset]).reduce_local(k, phi, psi_l, psi_r)
            i = i+1
        # Step 2 : Gather local Results
        if pid == 0:
            for i in range(1, nprocs):
                gt.extend(comm.recv(source=i, tag=TAG_COMM_REDUCE)['c'])
        else:
            comm.send({'c': gt}, dest=0, tag=TAG_COMM_REDUCE)
        # Step 3 : Global Reduction
        return gt.reduce_global(psi_n) if pid == 0 else None

    def uacc(self, k, phi, psi_n, psi_l, psi_r):
        """Upward accumulation skeleton for distributed tree

        The parameters must respect these equalities (closure property):
        * k(l, b, r) = psi_n(l, phi(b), r)
        * psi_n(psi_n(x, l, y), b, r) = psi_n(x, psi_l(l,b,r), y)
        * psi_n(l, b, psi_n(x, r, y)) = psi_n(x, psi_r(l,b,r), y)

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
        assert self.__distribution != []
        # Step 1 : Local Upwards Accumulation
        gt = Segment([None] * self.__nb_segs)
        lt2 = SList([None] * self.__nb_segs)
        i = 0
        for (start, offset) in self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]:
            (top, res) = Segment(self.__content[start:start + offset]).uacc_local(k, phi, psi_l, psi_r)
            gt[i] = top
            lt2[i] = res
            i = i + 1

        # Step 2 : Gather local Results
        if pid == 0:
            for iproc in range(1, nprocs):
                gt.extend(comm.recv(source=iproc, tag=TAG_COMM_UACC_1)['c'])
        else:
            comm.send({'c': gt}, dest=0, tag=TAG_COMM_UACC_1)

        # Step 3 : Global Upward Accumulation
        gt2 = None
        if pid == 0:
            gt2 = gt.uacc_global(psi_n)
            for i in range(len(gt2)):
                if gt2[i].is_node():
                    gt2[i] = TaggedValue((gt2.get_left(i).get_value(), gt2.get_right(i).get_value()), gt2[i].get_tag())

        # Step 4 : Distributing Global Result
        start = 0
        if pid == 0:
            for iproc in range(nprocs):
                iproc_off = self.__distribution[iproc]
                if iproc != 0:
                    comm.send({'g': gt2[start: start + iproc_off]}, dest=iproc, tag=TAG_COMM_UACC_2)
                start = start + iproc_off
        else:
            gt2 = comm.recv(source=0, tag=TAG_COMM_UACC_2)['g']

        # Step 5 : Local Updates
        content = SList()
        for i in range(len(self.__global_index[self.__start_index: self.__start_index + self.__nb_segs])):
            (start, offset) = self.__global_index[self.__start_index: self.__start_index + self.__nb_segs][i]
            if gt[i].is_node():
                (lc, rc) = gt2[i].get_value()
                val = Segment(self.__content[start:start + offset]).uacc_update(lt2[i], k, lc, rc)
            else:
                val = lt2[i]
            content.extend(val)

        return PTree.init(self, content)

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
        # Step 1 : Computing Local Intermediate Values
        gt = Segment([None] * self.__nb_segs)
        i = 0
        for (start, offset) in self.__global_index[self.__start_index: self.__start_index + self.__nb_segs]:
            seg = Segment(self.__content[start:start + offset])
            if seg.has_critical():
                gt[i] = seg.dacc_path(phi_l, phi_r, psi_u)
            else:
                gt[i] = TaggedValue(seg[0].get_value(), "L")
            i = i + 1
        # Step 2 : Gather Local Results
        if pid == 0:
            for iproc in range(1, nprocs):
                gt.extend(comm.recv(source=iproc, tag=TAG_COMM_DACC_1)['c'])
        else:
            comm.send({'c': gt}, dest=0, tag=TAG_COMM_DACC_1)
        # Step 3 : Global Downward Accumulation
        gt2 = (gt.dacc_global(psi_d, c) if pid == 0 else None)
        # Step 4 : Distributing Global Result
        if pid == 0:
            start = 0
            for iproc in range(nprocs):
                iproc_off = self.__distribution[iproc]
                if iproc != 0:
                    comm.send({'g': gt2[start: start + iproc_off]}, dest=iproc, tag=TAG_COMM_UACC_2)
                start = start + iproc_off
        else:
            gt2 = comm.recv(source=0, tag=TAG_COMM_UACC_2)['g']
        # Step 5 : Local Downward Accumulation
        content = SList([])
        for i in range(len(self.__global_index[self.__start_index: self.__start_index + self.__nb_segs])):
            (start, offset) = self.__global_index[self.__start_index: self.__start_index + self.__nb_segs][i]
            content.extend(Segment(self.__content[start:start + offset]).dacc_local(gl, gr, gt2[i].get_value()))
        return PTree.init(self, content)

    def zip(self, pt):
        """Zip skeleton for distributed tree

        Precondition
        -------------
        The distributions of self and pt should be the same

        Parameters
        ----------
        pt : :obj:`PTree`
            The PTree to zip with the current instance
        """
        assert self.__distribution == pt.__distribution
        content = SList([])
        for i in range(len(self.__global_index[self.__start_index: self.__start_index + self.__nb_segs])):
            (start, offset) = self.__global_index[self.__start_index: self.__start_index + self.__nb_segs][i]
            content.extend(Segment(self.__content[start:start+offset])
                               .zip(Segment(pt.__content[start:start+offset])))
        return PTree.init(self, content)

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
        assert self.__distribution == pt.__distribution
        content = SList([])
        for i in range(len(self.__global_index[self.__start_index: self.__start_index + self.__nb_segs])):
            (start, offset) = self.__global_index[self.__start_index: self.__start_index + self.__nb_segs][i]
            content.extend(
                Segment(self.__content[start:start + offset]).map2(f, Segment(pt.__content[start:start + offset])))
        return PTree.init(self, content)

    def get_full_index(self):
        def f(x, y):
            (x1, y1) = x
            (x2, y2) = y
            return x1 + y1, y2
        return SList(self.__global_index.scanr(f))

    def to_seq(self):
        full_content = []
        if pid == 0:
            full_index = self.get_full_index()
            res = LTree([None] * full_index.length())
            full_content.extend(self.__content)
            for iproc in range(1, nprocs):
                full_content.extend(comm.recv(source=iproc, tag=TAG_TO_SEQ)['c'])

            for i in range(full_index.length()):
                (start, offset) = full_index[i]
                res[i] = full_content[start:start + offset]
            return res
        else:
            comm.send({'c': self.__content}, dest=0, tag=TAG_TO_SEQ)
            return None
