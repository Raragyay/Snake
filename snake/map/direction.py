# coding=utf-8
"""Definition of Enum Direc. Used in class pos."""
from enum import Enum, unique


@unique
class Direc(Enum):
    """
    Directions on the game plane.
    Enum is so that we can give more interpretable values.
    Instead of using 0,1,2,3,4, it's easier to read when we use cardinal(?) directions.
    """
    NONE = 0
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4

    @staticmethod
    def opposite(direc):
        """
        :param direc: The direction given, of class Direc.
        :return: The opposite of the direction given.
        """
        if direc == Direc.LEFT:
            return Direc.RIGHT
        elif direc == Direc.RIGHT:
            return Direc.LEFT
        elif direc == Direc.UP:
            return Direc.DOWN
        elif direc == Direc.DOWN:
            return Direc.UP
        else:
            return Direc.NONE
