"""
A module to represent a point
"""
from abc import ABC

class Point_Interface(ABC):
    """Point interface to represent point of n dimensions"""

    def __repr__(self):
        pass

    def __eq__(self, other):
        pass

    def __add__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def distance(self, other):
        pass
