"""
A module of parallel arrays and associated skeletons

class PArray2D: parallel arrays.
"""
from typing import Callable, TypeVar, Generic, Optional
from enum import Enum

from pyske.core import SList, PList
from pyske.core.array import array_interface
from pyske.core.array.array_interface import Distribution
from pyske.core.array.sarray2d import SArray2D
from pyske.core.support import parallel as parimpl

_PID: int = parimpl.PID
_NPROCS: int = parimpl.NPROCS
_COMM = parimpl.COMM

T = TypeVar('T')  # pylint: disable=invalid-name
V = TypeVar('V')  # pylint: disable=invalid-name


def _local_index(distribution: Enum, col_size: int, line_size: int, pid: int):
    local_sizes = SList([])
    for i in range(_NPROCS):
        if distribution == Distribution.LINE:
            local_sizes.append(parimpl.local_size(i, line_size))
        else:
            local_sizes.append(parimpl.local_size(i, col_size))
    start_indexes = local_sizes.scanl(lambda x, y: x + y, 0)
    if distribution == Distribution.LINE:
        return (start_indexes[pid], start_indexes[pid] + local_sizes[pid] - 1), (0, col_size - 1)
    return (0, line_size - 1), (start_indexes[pid], start_indexes[pid] + local_sizes[pid] - 1)


class PArray2D(array_interface.Array2D, Generic[T]):
    # pylint: disable=protected-access
    """
    Distributed arrays
    """

    def __init__(self: 'PArray2D[T]'):
        super().__init__()
        self.__global_index = ((-1, -1), (-1, -1))
        self.__local_index = ((-1, -1), (-1, -1))
        self.__content = SArray2D([], -1, -1)
        self.__distribution = [((-1, -1), (-1, -1)) for _ in range(0, _NPROCS)]
        self.__distribution_direction = Distribution.LINE

    def __str__(self: 'PArray2D[T]') -> str:
        return "PID[" + str(_PID) + "]:\n" + \
               "  global_index: " + str(self.__global_index) + "\n" + \
               "  local_index: " + str(self.__local_index) + "\n" + \
               "  distribution: " + str(self.__distribution) + "\n" + \
               "  content: \n" + str(self.__content) + "\n"

    @staticmethod
    def init(value_at: Callable[[int, int], V], distribution: Distribution,
             col_size: int = _NPROCS,
             line_size: int = _NPROCS) -> 'PArray2D[V]':
        """
        Return an array built using a function per line on each processor

        :param value_at: binary function
        :param distribution: the distribution direction (LINE, COLUMN)
        :param col_size: number of columns
        :param line_size: number of lines
        :return: an 2d array of the given line and column size, where for all valid line column
            i, j, the value at this index is value_at(i, j)
        """
        assert _NPROCS <= col_size
        assert _NPROCS <= line_size

        parray2d = PArray2D()
        parray2d.__global_index = ((0, line_size - 1), (0, col_size - 1))

        parray2d.__local_index = _local_index(distribution, col_size, line_size, _PID)

        content = []
        for line in range(parray2d.__local_index[0][0], parray2d.__local_index[0][1] + 1):
            for column in range(parray2d.__local_index[1][0], parray2d.__local_index[1][1] + 1):
                content.append(value_at(line, column))
        local_line_size = parray2d.__local_index[0][1] - parray2d.__local_index[0][0] + 1
        local_col_size = parray2d.__local_index[1][1] - parray2d.__local_index[1][0] + 1
        parray2d.__content = SArray2D(content, local_line_size, local_col_size)

        parray2d.__distribution_direction = distribution
        parray2d.__distribution = [
            _local_index(parray2d.__distribution_direction, col_size, line_size, i) for i in
            range(_NPROCS)]

        return parray2d

    def distribute(self: 'PArray2D[T]') -> 'PArray2D[T]':
        """
        Distribute line to column
        """
        parray2d = PArray2D()
        parray2d.__global_index = self.__global_index

        col_size = self.__global_index[1][1] - self.__global_index[1][0] + 1
        line_size = self.__global_index[0][1] - self.__global_index[0][0] + 1

        parray2d.__local_index = _local_index(Distribution.COLUMN, col_size, line_size, _PID)
        parray2d.__distribution_direction = Distribution.COLUMN
        parray2d.__distribution = [
            _local_index(parray2d.__distribution_direction, col_size, line_size, i) for i in
            range(_NPROCS)]
        local_line_size = parray2d.__local_index[0][1] - parray2d.__local_index[0][0] + 1
        local_col_size = parray2d.__local_index[1][1] - parray2d.__local_index[1][0] + 1

        # update content for each process
        for i in range(0, _NPROCS):
            content_to_send = []
            for j in range(len(self.__content)):
                if j % col_size in range(parray2d.__distribution[i][1][0],
                                         parray2d.__distribution[i][1][1] + 1):
                    content_to_send.append(self.__content.values[j])
            if i == _PID:
                content = _COMM.gather(content_to_send, i)
                # flatten the list
                content = [item for items in content for item in items]
                parray2d.__content = SArray2D(content, local_line_size, local_col_size)
            else:
                _COMM.gather(content_to_send, i)

        return parray2d

    def map(self: 'PArray2D[T]', unary_op: Callable[[T], V]) -> 'PArray2D[V]':
        """
        Apply a function to all the elements.

        The returned array has the same shape (same size, same distribution)
        than the initial array.
        """
        self.__content = self.__content.map(unary_op)
        return self

    def reduce(self: 'PArray2D[T]', binary_op: Callable[[T, T], T],
               neutral: Optional[T] = None) -> T:
        """
        Reduce an array of value to one value.

        :param binary_op: a binary associative and commutative operation
        :param neutral: (optional):
            a value that should be a neutral element for the operation,
            i.e. for all element e,
                ``binary_op(neutral, e) == binary_op(e, neutral) == e``.
            If this argument is omitted the list should not be empty.
        :return: a value
        """
        if neutral is None:
            assert self.__global_index != ((-1, -1), (-1, -1))
            partial = self.__content.reduce(binary_op)
        else:
            partial = self.__content.reduce(binary_op, neutral)
        partials = SArray2D(_COMM.allgather(partial), self.__content.line_size,
                            self.__content.column_size)
        return partials.reduce(binary_op, neutral)

    def get_partition(self: 'PArray2D[T]') -> 'PList[SArray2D[T]]':
        contents = _COMM.allgather(self.__content)
        p_list = PList().init(lambda i: contents[i], _NPROCS)
        return p_list
