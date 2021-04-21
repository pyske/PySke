"""
Execution of fft.py
"""

import math
import gc
from pyske.core import PList, par
from pyske.core import Timing
from pyske.examples.list import util
from pyske.examples.list.fft import fft


# -------------- Execution --------------

def _is_power_of_2(num: int) -> bool:
    return num == round(2 ** (math.log2(num)))


def _main():
    size, num_iter, _ = util.standard_parse_command_line(data_arg=False)
    assert _is_power_of_2(size), "The size should be a power of 2."
    assert _is_power_of_2(len(par.procs())), "The number of processors should be a power of 2."
    input_list = PList.init(lambda _: 1.0, size)
    timing = Timing()
    gc.disable()
    for iteration in range(1, 1 + num_iter):
        timing.start()
        result = fft(input_list)
        timing.stop()
        gc.collect()
        result = result.to_seq()[0]
        util.print_experiment(result, timing.get(), par.at_root, iteration)


if __name__ == '__main__':
    _main()
