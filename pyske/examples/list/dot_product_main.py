"""
Execution of dot_product.py
"""

import gc
import random
from pyske.examples.list.dot_product import opt_dot_product, dot_product
from pyske.core import par, Timing, PList as DPList
from pyske.core.opt import fun as opt
from pyske.core.opt.list import PList
from pyske.examples.list.util import rand_list, print_experiment, dot_product_parser


# -------------- Execution -----------------


def __main():
    def __compute():
        if test == _DIRECT:
            return opt_dot_product(pl1, pl2)
        if test == _HAND:
            return dot_product(pl1, pl2)
        if test == _EVAL:
            return opt_dot_product(PList.raw(pl1), PList.raw(pl2), uncurry=opt.uncurry).eval()
        return opt_dot_product(PList.raw(pl1), PList.raw(pl2), uncurry=opt.uncurry).run()

    # Command-line arguments parsing
    parser = dot_product_parser()
    args = parser.parse_args()
    size = args.size
    test = args.test

    # Creation of input lists
    random.seed(42)
    pl1 = rand_list(DPList, size)
    pl2 = rand_list(DPList, size)

    # Execution and timing
    time = Timing()
    par.at_root(lambda: print("Test:\t", test))
    for iteration in range(0, args.iter):
        gc.collect()
        gc.disable()
        par.barrier()
        time.start()
        result = __compute()
        time.stop()
        print_experiment(result, time.get(), par.at_root, iteration)


if __name__ == '__main__':
    _DIRECT = '_DIRECT'
    _HAND = 'hand_optimized'
    _OPT = 'optimized'
    _EVAL = 'evaluated'
    __main()
