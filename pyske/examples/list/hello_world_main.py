"""
Example: various manipulations on a parallel list
"""

from operator import add, concat
from pyske.core import PList, SList, par

__all__ = []

__MSG = "hello world!"


def __main():
    parallel_list1 = PList.init(lambda i: __MSG[i], len(__MSG))
    parallel_list2 = PList.init(lambda x: x, len(__MSG))
    parallel_list4 = parallel_list1.map(lambda x: x.capitalize()).zip(parallel_list2)
    parallel_list6 = parallel_list4.map(lambda x: x[0]).mapi(lambda i, x: (i, x))
    parallel_list7 = parallel_list6.map(lambda x: x[1])
    parallel_list8 = parallel_list7.map(lambda x: 1)
    size = parallel_list8.reduce(lambda x, y: x + y, 0)
    parallel_list9 = parallel_list7.get_partition()
    parallel_list10 = parallel_list9.map(lambda l: SList(l).filter(lambda c: c != 'O')).flatten()
    parallel_list11 = PList.from_seq(["Hello World!"])
    filtered = SList(parallel_list10.get_partition().reduce(concat, [])).reduce(add)
    str1 = SList(parallel_list9.reduce(add)).reduce(add)
    str2 = parallel_list11.to_seq()[0]
    par.at_root(lambda:
                print(f'Capitalized: \t{str1}\n'
                      f'Identity:\t{str2}\n'
                      f'Length:\t\t{size}\n'
                      f'Filtered:\t{filtered}'))


if __name__ == '__main__':
    __main()
