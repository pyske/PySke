import functools
from operator import add

from pyske.core.support import parallel
from pyske.core.support.list import scan
from pyske.core.util.par import procs
from pyske.core.util.fun import dist_euclidean

__all__ = ['Distribution']

class Distribution:

    def __init__(self, distr, global_index):
        self.__distr = distr
        self.__global_index = global_index

    def __eq__(self, other):
        if isinstance(other, Distribution):
            return self.__distr == other.__distr \
                   and self.__global_index == other.__global_index
        else:
            return False

    @property
    def distribution(self):
        return self.__distr

    @property
    def global_index(self):
        return self.__global_index

    def is_valid(self, size: int) -> bool:
        if len(self.__distr) != parallel.NPROCS:
            return False
        for num in self.__distr:
            if num < 0:
                return False
        return size == functools.reduce(add, self.__distr, 0)

    @staticmethod
    def balanced_segs(sizes: 'list [int]') -> 'Distribution':
        distr = [parallel.local_size(pid, len(sizes)) for pid in procs()]
        global_index = []
        if sizes:
            ptr = 0
            for nb_seg in distr:
                acc_sizes = 0
                for i in range(nb_seg):
                    global_index.append((acc_sizes, sizes[ptr]))
                    acc_sizes += sizes[ptr]
                    ptr += 1
        return Distribution(distr, global_index)

    @staticmethod
    def balanced_tree(sizes: 'list [int]') -> 'Distribution':
        distr = [0] * parallel.NPROCS
        global_index = []
        if sizes:
            nb_segment = len(sizes)
            total_size = functools.reduce(add, sizes, 0)
            avg_elements = int(total_size / max(1, parallel.NPROCS))
            iterator_sizes = 0
            accumulated_size = 0
            for iterator_pid in range(parallel.NPROCS):
                seg_by_pid = 0
                if accumulated_size is 0 and iterator_sizes < nb_segment:
                    global_index.append((accumulated_size, sizes[iterator_sizes]))
                    accumulated_size += sizes[iterator_sizes]
                    iterator_sizes += 1
                    seg_by_pid += 1
                while(iterator_sizes < nb_segment and
                      (dist_euclidean(accumulated_size + sizes[iterator_sizes], avg_elements) < dist_euclidean(accumulated_size,
                                                                                                       avg_elements)
                       or iterator_pid == parallel.NPROCS - 1)):
                    global_index.append((accumulated_size, sizes[iterator_sizes]))
                    accumulated_size += sizes[iterator_sizes]
                    iterator_sizes += 1
                    seg_by_pid += 1
                accumulated_size = 0
                distr[iterator_pid] = seg_by_pid

        return Distribution(distr, global_index)

    def to_pid(self, index: int, value):
        indices = scan(self.__distr, add, 0)
        indices.pop(0)
        for (pid, bound) in enumerate(indices):
            if index < bound:
                return pid, (index, value)
        return None  # unreachable if index is valid
