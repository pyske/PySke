"""
A module to represent a point
"""

from math import sqrt


class Point(object):
    """A class to represent a point"""

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __repr__(self):
        return "(%s, %s)" % (self.__x, self.__y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.__x == other.x and self.__y == other.__y
        return False

    @property
    def x(self):
        """X getter"""
        return self.__x

    @property
    def y(self):
        """Y getter"""
        return self.__y

    def distance(self, other: 'Point'):
        """
        Returns the distance from another point.

        Examples::

            >>> from pyske.core.util.point import Point
            >>> p1 = Point(5,5)
            >>> p2 = Point(5,7)
            >>> p1.distance(p2)
            2.0

        :param other: a point
        :return: distance from other point

        """
        dx = self.__x - other.x
        dy = self.__y - other.y
        return sqrt(dx ** 2 + dy ** 2)
