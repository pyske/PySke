"""
A module to represent a 3D point
"""

from math import sqrt
from pyske.core.util.point_Interface import Point_Interface


class Point_3D(Point_Interface):
    """A class to represent a 3D point"""

    def __init__(self, x=0, y=0, z=0):
        self.__x = x
        self.__y = y
        self.__z = z

    def __repr__(self):
        return "(%s, %s, %s)" % (self.__x, self.__y, self.__z)

    def __eq__(self, other):
        if isinstance(other, Point_3D):
            return self.__x == other.__x and self.__y == other.__y and self.__z == other.__z
        return False

    def __add__(self, other):
        """
        Addition of two points

        Examples::

            >>> p1 = Point_3D(5,5,2)
            >>> p2 = Point_3D(5,7,1)
            >>> p1 + p2
            (10, 12, 3)
        """
        if isinstance(other, Point_3D):
            return Point_3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        """
        Multiplication by a point or a scalar

        Examples::

            >>> p1 = Point_3D(5,5,2)
            >>> p2 = Point_3D(5,7,1)
            >>> p1 * 5
            (25, 25, 10)
            >>> p1 * p2
            (25, 35, 2)
        """
        if isinstance(other, Point_3D):
            return Point_3D(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, int) or isinstance(other, float):
            return Point_3D(self.x * other, self.y * other, self.z * other.z)

    def __truediv__(self, other):
        if isinstance(other, int):
            return Point_3D(self.x / other, self.y / other, self.z / other)

    @property
    def x(self):
        """X getter"""
        return self.__x

    @property
    def y(self):
        """Y getter"""
        return self.__y

    @property
    def z(self):
        """Z getter"""
        return self.__z

    def distance(self, other):
        """
        Returns the distance from another 3D point.

        Examples::

            >>> from pyske.core.util.point_2D import Point_2D
            >>> p1 = Point_3D(5,5,2)
            >>> p2 = Point_3D(5,7,1)
            >>> p1.distance(p2)
            2.24

        :param other: a point
        :return: distance from other point

        """
        dx = self.__x - other.x
        dy = self.__y - other.y
        dz = self.__z - other.z
        return sqrt(dx ** 2 + dy ** 2 + dz ** 2)
