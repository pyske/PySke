"""
Example of use of filtering and then redistribution
"""
import sys
import random
from pyske.core.list.plist import PList
from pyske.core.util import par, timing


def _is_even(num):
    """
    Checks whether its argument is even.
    :param num: int
    :return: bool
    """
    return num % 2 == 0


def _main():
    time = timing.Timing()
    # Generating a parallel list of the size specified on the command line or 1000
    size = 1000
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    data = PList.init(lambda _: 50 + random.randint(0, 100), size)
    par.barrier()
    # start timing
    time.start()
    # filter out odd values and get the distribution after balancing
    distr = data.filter(_is_even).balance().get_partition().map(len).to_seq()
    # stop timing
    time.stop()
    max_elapsed, avg_elapsed, all_elapsed = time.get()
    # output at processor 0
    par.at_root(lambda:
                print(f'Distribution: \t{distr}\nTime (max): \t{max_elapsed}\n'
                      f'Time (avg): \t{avg_elapsed}\nTime (all): \t{all_elapsed}'))


_main()
