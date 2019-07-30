"""
Example: various manipulations on a parallel list
"""

import operator
from pyske.core import PList, SList, par

__all__ = []

__MSG = "hello world!"


def __main():
    pl1 = PList.init(lambda i: __MSG[i], len(__MSG))
    pl2 = PList.init(lambda x: x, len(__MSG))
    pl4 = pl1.map(lambda x: x.capitalize()).zip(pl2)
    pl6 = pl4.map(lambda x: x[0]).mapi(lambda i, x: (i, x))
    pl7 = pl6.map(lambda x: x[1])
    pl8 = pl7.map(lambda x: 1)
    size = pl8.reduce(lambda x, y: x + y, 0)
    pl9 = pl7.get_partition()
    pl10 = pl9.map(lambda l: SList(l).filter(lambda c: c != 'O')).flatten()
    pl11 = PList.from_seq(["Hello World!"])
    filtered = SList(pl10.get_partition().reduce(operator.concat, [])).reduce(operator.add)
    str1 = SList(pl9.reduce(operator.add)).reduce(operator.add)
    str2 = pl11.to_seq()[0]
    par.at_root(lambda:
                print(f'Capitalized: \t{str1}\n'
                      f'Identity:\t{str2}\n'
                      f'Length:\t\t{size}\n'
                      f'Filtered:\t{filtered}'))


__main()
