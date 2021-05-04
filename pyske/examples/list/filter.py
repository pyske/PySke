"""
Example of use of filtering and then redistribution
"""

from pyske.core.util import fun
from pyske.core import PList, Distribution


# ----------------- Example -------------------

def _filter_even(input_list: PList) -> Distribution:
    return input_list.filter(fun.is_even).balance().distribution
