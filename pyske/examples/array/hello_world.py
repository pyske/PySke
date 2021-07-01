"""
Example: various manipulations on a parallel array
"""

from pyske.core.array.parray2d import PArray2D
from pyske.core.array.array_interface import Distribution
from pyske.core.array.sarray2d import SArray2D


def __main():
    col_size = 6
    line_size = 12

    print("Line initialization")
    parray2d_line_init = PArray2D.init(lambda line, column: line * col_size + column,
                                       Distribution.LINE, col_size, line_size)
    print(parray2d_line_init)

    print("Line to column distribution")
    parray2d_column = parray2d_line_init.distribute(Distribution.COLUMN)
    print(parray2d_column)

    print("Column to line distribution")
    parray2d_line = parray2d_column.distribute(Distribution.LINE)
    print(parray2d_line)

    print("Column initialization")
    parray2d_column_init = PArray2D.init(lambda line, column: line * col_size + column,
                                         Distribution.COLUMN, col_size, line_size)
    print(parray2d_column_init)

    print("Reduce Test")
    print(parray2d_column_init.reduce(lambda x, y: x + y, 0))
    print(parray2d_column_init.reduce(lambda x, y: x + y))
    print(parray2d_line_init.reduce(lambda x, y: x + y, 0))
    print(parray2d_column.reduce(lambda x, y: x + y, 0))
    print(PArray2D().reduce(lambda x, y: x + y, 0))

    print("Mapped array")
    parray2d_map = parray2d_line_init.map(lambda x: x + 1)
    print(parray2d_map)

    print("Sarray initialization")
    sarray2d = SArray2D.init(lambda line, column: line * col_size + column, Distribution.LINE,
                             col_size, line_size)
    print(sarray2d)

    print("Get partition")
    print(parray2d_column_init.get_partition())

    b_sarray2d = SArray2D.init(lambda line, column: 1, Distribution.LINE, col_size, line_size)

    print("Map2 array")
    print(sarray2d.map2(lambda x, y: x + y, b_sarray2d))
    print(parray2d_line_init.map2(lambda x, y: x + y, parray2d_line_init))
    print(parray2d_column_init.map2(lambda x, y: x + y, parray2d_column))

    print("To seq")
    print(parray2d_column.to_seq())


if __name__ == '__main__':
    __main()
