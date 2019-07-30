"""
core: data structures and associated skeletons

Classes:
    * PList
    * SList
    * Timing

Modules:
    * par
    * fun
    * opt
"""

from pyske.core.list import PList, SList
from pyske.core.util.timing import Timing
from pyske.core.util import par
from pyske.core.util import fun

__all__ = ['PList', 'SList', 'Timing', 'par', 'fun']
