from pyske.core.list.slist import SList
from pyske.core.support.parallel import *
from pyske.core.support.interval import *


class PList:
    """Distributed lists"""

    def __init__(self):
        self.__content = SList([])
        self.__global_size = 0
        self.__local_size = 0
        self.__start_index = 0
        self.__distribution = [0 for i in range(0, nprocs)]

    def __get_shape(self):
        p = PList()
        p.__local_size = self.__local_size
        p.__global_size = self.__global_size
        p.__distribution = self.__distribution
        p.__start_index = self.__start_index
        return p

    def __str__(self):
        return "pid[" + str(pid) + "]:\n" + \
               "  global_size: " + str(self.__global_size) + "\n" + \
               "  local_size: " + str(self.__local_size) + "\n" + \
               "  start_index: " + str(self.__start_index) + "\n" + \
               "  distribution: " + str(self.__distribution) + "\n" + \
               "  content: " + str(self.__content) + "\n"

    def invariant(self):
        type(self.__content) is SList
        prefix = SList(self.__distribution).scan(add, 0)
        assert len(self.__content) == self.__local_size
        assert self.__distribution[pid] == self.__local_size
        assert self.__start_index ==  prefix[pid]
        assert prefix[nprocs] == self.__global_size


    def length(self):
        return self.__global_size

    @staticmethod
    def init(f, size):
        assert (size >= 0)
        p = PList()
        p.__global_size = size
        p.__local_size = local_size(size)
        p.__distribution = [local_size_pid(i, size) for i in range(0, nprocs)]
        p.__start_index = SList(p.__distribution).scanl(lambda x, y: x + y, 0)[pid]
        p.__content = SList([f(i) for i in range(p.__start_index, p.__start_index + p.__local_size)])
        p.__distribution = [local_size_pid(i, size) for i in range(0, nprocs)]
        return p

    def map(self, f):
        p = self.__get_shape()
        p.__content = self.__content.map(f)
        return p

    def mapi(self, f):
        p = self.__get_shape()
        p.__content = self.__content.mapi(lambda i, x: f(i+self.__start_index, x))
        return p

    def map2(self, f, pl):
        assert (self.__distribution == pl.__distribution)
        p = self.__get_shape()
        p.__content = self.__content.map2(f, pl.__content)
        return p

    def map2i(self, f, pl):
        assert (self.__distribution == pl.__distribution)
        p = self.__get_shape()
        p.__content = self.__content.map2i(lambda i, x, y: f(i+self.__start_index, x, y), pl.__content)
        return p

    def zip(self, pl):
        return self.map2(lambda x, y: (x, y), pl)

    def filter(self, p):
        return self.get_partition().map(lambda l: l.filter(p)).flatten()

    def get_partition(self):
        p = PList()
        p.__content = SList([self.__content])
        p.__global_size = nprocs
        p.__local_size = 1
        p.__start_index = pid
        p.__distribution = [1 for i in range(0, nprocs)]
        return p

    def flatten(self):
        p = PList()
        p.__content = self.__content.reduce(lambda x, y: x + y, [])
        p.__local_size = len(p.__content)
        p.__distribution = comm.allgather(p.__local_size)
        p.__start_index = SList(p.__distribution).scanl(lambda x, y: x + y, 0)[pid]
        p.__global_size = SList(p.__distribution).reduce(lambda x, y: x + y)
        return p

    def reduce(self, op, e=None):
        if e is None:
            assert (self.__global_size >= 1)
            partial = None if self.__local_size == 0 else SList(self.__content).reduce(op)
            partials = SList(comm.allgather(partial)).filter(lambda x: x is not None)
        else:
            # assert: (op, e) form a monoid
            partial = SList(self.__content).reduce(op, e)
            partials = SList(comm.allgather(partial))
        return partials.reduce(op, e)

    def map_reduce(self, f, op, e=None):
        if e is None:
            assert (self.__global_size >= 1)
            partial = None if self.__local_size == 0 else SList(self.__content).map_reduce(f, op)
            partials = SList(comm.allgather(partial)).filter(lambda x: x is not None)
        else:
            # assert: (op, e) form a monoid
            partial = SList(self.__content).map_reduce(f, op, e)
            partials = SList(comm.allgather(partial))
        return partials.reduce(op, e)

    def scanr(self, op):
        assert (self.__global_size > 0)
        p = self.__get_shape()
        partials = self.__content.scanr(op)
        last = partials[self.__local_size - 1]
        acc, _ = scan(op, last)
        if pid != 0:
            for i in range(0, len(partials)):
                partials[i] = op(acc, partials[i])
        p.__content = partials
        return p

    def scanl(self, op, e):
        p = self.__get_shape()
        partials, last = self.__content.scanl_last(op, e)
        acc, _ = scan(op, last)
        if pid != 0:
            for i in range(0, len(partials)):
                partials[i] = op(acc, partials[i])
        p.__content = partials
        return p

    def scanl_last(self, op, e):
        p = self.__get_shape()
        partials, last = self.__content.scanl_last(op, e)
        acc, red = scan(op, last)
        if pid != 0:
            for i in range(0, len(partials)):
                partials[i] = op(acc, partials[i])
        p.__content = partials
        return p, red

    def distribute(self, target_distr):
        assert (is_distribution(target_distr, self.__global_size))
        source_distr = self.__distribution
        source_bounds = bounds(source_distr)
        target_bounds = bounds(target_distr)
        local_interval = source_bounds[pid]
        bounds_to_send = target_bounds.map(lambda i: intersection(i, local_interval))
        msgs = [slice(self.__content, shift(inter, -self.__start_index)) for inter in bounds_to_send]
        slices = comm.alltoall(msgs)
        p = PList()
        p.__content = SList(slices).flatten()
        p.__local_size = target_distr[pid]
        p.__global_size = self.__global_size
        p.__start_index = SList(target_distr).scanl(add, 0)[pid]
        p.__distribution = target_distr
        return p

    def balance(self):
        return self.distribute(balanced_distribution(self.__global_size))

    def gather(self, pid):
        assert (pid in procs())
        distr = [self.length() if i == pid else 0 for i in procs()]
        return self.distribute(distr)

    def gather_at_root(self):
        return self.gather(0)

    def scatter(self, pid):
        assert (pid in procs())
        def select(i, l):
            if i == pid:
                return l
            else:
                return []
        at_pid = self.get_partition().mapi(select).flatten()
        return at_pid.distribute(balanced_distribution(at_pid.length()))

    def scatter_from_root(self):
        return self.scatter(0)

    def scatter_range(self, r):
        def select(i, x):
            if i in r:
                return x
            else:
                return None
        def notNone(x):
            return not (x is None)
        selected = self.mapi(select).filter(notNone)
        return selected.distribute(balanced_distribution(selected.length()))

    @staticmethod
    def from_seq(l):
        p = PList()
        if pid == 0:
            p.__content = SList(l)
            p.__distribution = [len(l)] + [0 for i in range(1, nprocs)]
        from_root = comm.bcast(p.__distribution, 0)
        p.__distribution = from_root
        p.__local_size = p.__distribution[pid]
        p.__global_size = p.__distribution[0]
        p.__start_index = SList(p.__distribution).scanl(add, 0)[pid]
        return p

    def to_seq(self):
        return SList(self.get_partition().reduce(lambda x, y: x + y, []))
