import functools
from operator import add
from typing import Tuple

from pyske.core import interface
from pyske.core.support import parallel
from pyske.core.support.list import scan
from pyske.core.util.par import procs
from pyske.core.util.fun import dist_euclidean

class Distribution(interface.Distribution):

    def is_valid(self, size: int) -> bool:
        if len(self) != parallel.NPROCS:
            return False
        for num in self:
            if num < 0:
                return False
        return size == functools.reduce(add, self, 0)

    @staticmethod
    def balanced(size: int) -> 'Distribution':
        distr = [parallel.local_size(pid, size) for pid in procs()]
        return Distribution(distr)

    @staticmethod
    def balanced_tree(sizes: 'list [int]') -> Tuple['Distribution', 'list[Tuple[int, int]]']:
        
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

        return Distribution(distr), global_index

    def to_pid(self, index: int, value):
        indices = scan(self, add, 0)
        indices.pop(0)
        for (pid, bound) in enumerate(indices):
            if index < bound:
                return pid, (index, value)
        return None  # unreachable if index is valid
