"""
Example: various manipulations on a parallel array
"""

from pyske.core.array.parray2d import PArray2D


def __main():
    col_size = 6
    line_size = 12
    parray2d = PArray2D.init(lambda line, column: line * col_size + column, col_size, line_size)
    #print(parray2d)
    parray2d = parray2d.distribute()
    print(parray2d)


if __name__ == '__main__':
    __main()
