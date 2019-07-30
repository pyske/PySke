"""
pyske.core.list: sequential and parallel lists.

Classes:
    * SList: sequential list.
    * PList: parallel list.
"""

from .plist import PList
from .slist import SList

__all__ = ['SList', 'PList']
