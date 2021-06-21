"""
Example: various manipulations on a parallel array
"""

from pyske.core.array.parray2d import PArray2D


def __main():
    col_size = 6
    line_size = 12

    print("Line initialization")
    parray2d_line_init = PArray2D.init_line(lambda line, column: line * col_size + column, col_size, line_size)
    print(parray2d_line_init)

    print("Line to column distribution")
    parray2d_column = parray2d_line_init.distribute()
    print(parray2d_column)

    print("Column initialization")
    parray2d_column_init = PArray2D.init_column(lambda line, column: line * col_size + column, col_size, line_size)
    print(parray2d_column_init)


if __name__ == '__main__':
    __main()
