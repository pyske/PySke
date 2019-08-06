"""
Example of use of filtering and then redistribution
"""

from pyske.core.util import fun
from pyske.core import PList, Distribution
from pyske.examples.list.util import standard_main


# ----------------- Example -------------------

def _filter_even(input_list: PList) -> Distribution:
    return input_list.filter(fun.is_even).balance().distribution


# ----------------- Execution -------------------

if __name__ == '__main__':
    standard_main(_filter_even, data_arg=False)
