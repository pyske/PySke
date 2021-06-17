"""
A module of parallel arrays and associated skeletons

class PArray2D: parallel arrays.
"""
from typing import Callable

from pyske.core.support import parallel as parimpl

_PID: int = parimpl.PID
_NPROCS: int = parimpl.NPROCS
_COMM = parimpl.COMM


class PArray2D:
    # pylint: disable=protected-access
    """
    Distributed arrays
    """

    def __init__(self):
        self.__global_index = 0
        self.__local_index = 0
        self.__content = []
        self.__distribution = [0 for _ in range(0, _NPROCS)]

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

        local_line_size = parimpl.local_size(_PID, line_size)
        if _PID == 0:
            lines_start_index = local_line_size * _PID
        else:
            lines_start_index = _COMM.recv(source=_PID - 1) + 1
        lines_stop_index = lines_start_index + local_line_size - 1
        if _PID != _NPROCS - 1:
            _COMM.send(lines_stop_index, _PID + 1)

        colums_start_index = 0
        colums_stop_index = col_size - 1

        parray2d.__local_index = ((lines_start_index, lines_stop_index),
                                  (colums_start_index, colums_stop_index))

        parray2d.__content = [value_at(i) for i in range(lines_start_index * col_size,
                                                         (lines_stop_index + 1) * col_size)]
        parray2d.__distribution = _COMM.allgather(parray2d.__local_index)

        return parray2d

    def distribute(self: 'PArray2D') -> 'PArray2D':
        parray2d = PArray2D()
        parray2d.__global_index = self.__global_index

        col_size = self.__global_index[1][1] - self.__global_index[1][0] + 1
        line_size = self.__global_index[0][1] - self.__global_index[0][0] + 1

        local_col_size = parimpl.local_size(_PID, col_size)
        if _PID == 0:
            colums_start_index = local_col_size * _PID
        else:
            colums_start_index = _COMM.recv(source=_PID - 1) + 1
        colums_stop_index = colums_start_index + local_col_size - 1
        if _PID != _NPROCS - 1:
            _COMM.send(colums_stop_index, _PID + 1)

        lines_start_index = 0
        lines_stop_index = line_size - 1

        parray2d.__local_index = ((lines_start_index, lines_stop_index),
                                  (colums_start_index, colums_stop_index))

        parray2d.__distribution = _COMM.allgather(parray2d.__local_index)

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
