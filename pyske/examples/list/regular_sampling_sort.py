"""
Parallel regular sampling sort
"""
import functools
from heapq import merge
from operator import and_
from pyske.core import PList, Distribution, par

__all__ = ['bcast', "pssr"]


# ------------------- Broadcast -------------------------

def bcast(input_list: PList, src_pid: int) -> PList:
    """
    Broadcast the data at source processor to all processors.

    Example::

        >>> from pyske.core import PList, par
        >>> bcast(PList.from_seq([42]), 0).to_seq() == list(map(lambda _: 42, par.procs()))
        True

    :param input_list: a parallel list.
    :param src_pid: the source processor identifier.
        Pre-condition: ``src_pid in par.procs()``
    :return: a parallel list.
    """
    assert src_pid in par.procs()
    size = input_list.distribution[src_pid]
    nprocs = len(par.procs())
    return input_list \
        .get_partition() \
        .mapi(lambda pid, lst: list(map(lambda _: lst, par.procs())) if pid == src_pid else []) \
        .flatten(Distribution([nprocs if pid == src_pid else 0 for pid in par.procs()])) \
        .distribute(Distribution(map(lambda _: 1, par.procs()))) \
        .flatten(Distribution(map(lambda _: size, par.procs())))


# ----------------- Parallel Sort -------------------------


def _merge2(sorted_list1, sorted_list2):
    return list(merge(sorted_list1, sorted_list2))


def _merge(sorted_lists):
    return functools.reduce(_merge2, sorted_lists, [])


def _index(sorted_list, element):
    assert sorted_list
    low = 0
    high = len(sorted_list) - 1
    while low < high:
        mid = low + int((high - low) / 2)
        if sorted_list[mid] == element:
            return mid
        if sorted_list[mid] < element:
            low = mid + 1
        else:
            high = mid - 1
    return low


def _slice(list_to_search, elements_to_find):
    indexes = list(map(lambda elt: _index(list_to_search, elt), elements_to_find))
    bounds = zip([0] + indexes, indexes + [len(list_to_search)])
    slices = map(lambda bound: list_to_search[bound[0]:bound[1]],
                 bounds)
    return list(slices)


def pssr(input_list: PList) -> PList:
    """
    Sort the input list.

    Sorts using ``<`` only.

    Example::

        >>> from pyske.core import PList
        >>> pssr(PList.init(lambda i: 10-i, 10)).to_seq()
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    :param input_list: a parallel list.
        Pre-condition: the size of the local lists should be at least
        equal to the number of processors.
    :return: a sorted list that is a permutation of ``input_list``.
    """
    nprocs = len(par.procs())
    if nprocs == 1:
        return input_list.get_partition().map(sorted).flatten()
    for local_size in input_list.distribution:
        assert local_size >= nprocs

    def permutation(index: int):
        return int(index / nprocs) + nprocs * (index % nprocs)

    def _sample(list_to_sample):
        if list_to_sample:
            size = len(list_to_sample)
            step = int(size / nprocs)
            return list_to_sample[step:size:step]
        return []

    locally_sorted = input_list.get_partition().map(sorted)
    first_samples = locally_sorted.map(_sample).gather(0).get_partition()
    second_samples = bcast(first_samples.map(_merge).map(_sample), 0)
    slices = locally_sorted.map2(_slice, second_samples).flatten()
    result = slices.permute(permutation).get_partition().map(_merge).flatten()
    return result


def _is_sorted_list(lst):
    return all(a <= b for a, b in zip(lst, lst[1:]))


def is_sorted(input_list: PList) -> bool:
    """Check if the list is sorted."""
    return input_list.get_partition().map(_is_sorted_list).reduce(and_, True)
