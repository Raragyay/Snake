# coding=utf-8
"""Definitions of class Point."""
from enum import Enum, unique


@unique
class PointType(Enum):
    """
    Unique point types for easy reference, instead of using dictionaries
    or straight-up numbers.
    Definition of Enum from Python: Enumeration members have human readable string representations.

    LU, UR, RD, and DL are enum members for different appearances of the snake.
    For example, if the snake was moving downwards, then it turned right,
    then the two 'edges' that that point of the body touched would be the top and the right edge.
    Therefore, it would be a PointType LU.
    """
    EMPTY = 0
    WALL = 1
    FOOD = 2
    HEAD_L = 100
    HEAD_U = 101
    HEAD_R = 102
    HEAD_D = 103
    BODY_LU = 104
    BODY_UR = 105
    BODY_RD = 106
    BODY_DL = 107
    BODY_HOR = 108
    BODY_VER = 109


class Point:
    """
    Point on the game map.
    This is the basis for practically everything, along with pos, since every Point on the map can be accessed by Pos.
    """

    def __init__(self):
        """
        Set the default PointType to empty.
        """
        self.__type = PointType.EMPTY

    @property
    def type(self):
        """
        :return: The type of the point. This is an PointType of class Enum.
        """
        return self.__type

    @type.setter
    def type(self, val):
        """
        Sets the type of the object. This uses the @property of python, which
        pretty means that when we call it, we can get the property, but we can use the
        same function to set the value.
        """
        self.__type = val
