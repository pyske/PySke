"""
A module of parallel arrays and associated skeletons

class PArray2D: parallel arrays.
"""
from typing import Callable
from enum import Enum

from pyske.core.support import parallel as parimpl

_PID: int = parimpl.PID
_NPROCS: int = parimpl.NPROCS
_COMM = parimpl.COMM

class Distribution(Enum):
    LINE = 'LINE'
    COLUMN = 'COLUMN'


def _local_index(distribution: str, col_size: int, line_size: int):
    if distribution == Distribution.LINE:
        local_size = parimpl.local_size(_PID, line_size)
        b_start_index = 0
        b_stop_index = col_size - 1
    else:
        local_size = parimpl.local_size(_PID, col_size)
        b_start_index = 0
        b_stop_index = line_size - 1

    if _PID == 0:
        a_start_index = local_size * _PID
    else:
        a_start_index = _COMM.recv(source=_PID - 1) + 1
    a_stop_index = a_start_index + local_size - 1
    if _PID != _NPROCS - 1:
        _COMM.send(a_stop_index, _PID + 1)

    if distribution == Distribution.LINE:
        return (a_start_index, a_stop_index), (b_start_index, b_stop_index)
    else:
        return (b_start_index, b_stop_index), (a_start_index, a_stop_index)


class PArray2D:
    # pylint: disable=protected-access
    """
    Distributed arrays
    """

    def __init__(self):
        self.__global_index = ((-1, -1), (-1, -1))
        self.__local_index = ((-1, -1), (-1, -1))
        self.__content = []
        self.__distribution = [0 for _ in range(0, _NPROCS)]
        self.__distribution_direction = Distribution.LINE

    def __str__(self) -> str:
        return "PID[" + str(_PID) + "]:\n" + \
               "  global_index: " + str(self.__global_index) + "\n" + \
               "  local_index: " + str(self.__local_index) + "\n" + \
               "  distribution: " + str(self.__distribution) + "\n" + \
               "  content: " + str(self.__content) + "\n"

    @staticmethod
    def init(value_at: Callable[[int], int], col_size: int = _NPROCS, line_size: int = _NPROCS):
        assert _NPROCS <= col_size
        assert _NPROCS <= line_size

        parray2d = PArray2D()
        parray2d.__global_index = ((0, line_size - 1), (0, col_size - 1))

        parray2d.__local_index = _local_index(Distribution.LINE, col_size, line_size)

        parray2d.__content = [value_at(i) for i in range(parray2d.__local_index[0][0] * col_size,
                                                         (parray2d.__local_index[0][1] + 1) * col_size)]
        parray2d.__distribution = _COMM.allgather(parray2d.__local_index)

        return parray2d

    def distribute(self: 'PArray2D') -> 'PArray2D':
        """
        Distribute line to column
        """
        parray2d = PArray2D()
        parray2d.__global_index = self.__global_index

        col_size = self.__global_index[1][1] - self.__global_index[1][0] + 1
        line_size = self.__global_index[0][1] - self.__global_index[0][0] + 1

        parray2d.__local_index = _local_index(Distribution.COLUMN, col_size, line_size)

        parray2d.__distribution = _COMM.allgather(parray2d.__local_index)
        parray2d.__distribution_direction = Distribution.COLUMN

        # update content for each process
        for i in range(0, _NPROCS):
            content_to_send = []
            for j in range(len(self.__content)):
                if j % col_size in range(parray2d.__distribution[i][1][0],
                                         parray2d.__distribution[i][1][1] + 1):
                    content_to_send.append(self.__content[j])
            if i == _PID:
                parray2d.__content = _COMM.gather(content_to_send, i)
                # flatten the list
                parray2d.__content = [item for items in parray2d.__content for item in items]
            else:
                _COMM.gather(content_to_send, i)

        return parray2d
