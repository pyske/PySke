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

        lines_start_index = local_line_size * _PID
        lines_stop_index = lines_start_index + local_line_size - 1
        colums_start_index = 0
        colums_stop_index = col_size - 1

        parray2d.__local_index = ((lines_start_index, lines_stop_index),
                                  (colums_start_index, colums_stop_index))

        parray2d.__content = [value_at(i) for i in range(lines_start_index * col_size,
                                                         (lines_stop_index + 1) * col_size)]
        parray2d.__distribution = [parimpl.local_size(_PID, line_size) * col_size for _ in
                                   range(0, _NPROCS)]
        return parray2d
