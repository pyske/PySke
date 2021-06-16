"""
Example: various manipulations on a parallel array
"""

from pyske.core.array.parray2d import PArray2D


def __main():
    parray2d = PArray2D.init(lambda x: x, 6, 12)
    print(parray2d)


if __name__ == '__main__':
    __main()
