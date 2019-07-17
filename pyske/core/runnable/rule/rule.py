from pyske.core.runnable.etree import ETree
from pyske.core.list.slist import SList as Core_SList

class Position(Core_SList):
    """
    SList used to describe a position in a tree
    """
    pass

class Rule:
    """
    Describe a transformation rule
    """
    def __init__(self, left, right, priority=-1):
        assert isinstance(left, ETree)
        assert isinstance(right, ETree)
        self.left = left
        self.right = right
        self.priority = priority

