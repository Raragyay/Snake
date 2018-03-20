# coding=utf-8
"""Definitions of class Pos."""

from snake.map.direction import Direc


class Pos:
    """
    This is an integer coordinate in a 2D plane.

    It starts at (0,0) in the top-left corner,
    extending rightwards for y and downwards for x.

    Why I do this, you ask? It's easier for maps, because the first index
    on a map is the rows, which looks nicer if it says x. :)
    """

    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y

    def __str__(self):
        return 'Pos: {},{}'.format(self.__x, self.__y)

    __repr__ = __str__

    # We do this so that it always returns the position,
    # even when the different methods are called.

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__x == other.__x and self.__y == other.__y
        return NotImplemented

    def __pos__(self):
        """
        This creates a copy of this position.
        :return:
        """
        return Pos(self.__x, self.__y)

    def __neg__(self):
        """
        This creates a copy of this object, but with negative x and y coordinates.
        :return:
        """
        return Pos(-self.__x, -self.__y)

    def __add__(self, other):
        if isinstance(self, other.__class__):
            return Pos(self.__x + other.__x, self.__y + other.__y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(self, other.__class__):
            return Pos(self.__x - other.__x, self.__y - other.__y)
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def manhattan_distance(p1, p2):
        """
        Returns manhattan distance from one point to another.
        Manhattan distance is the distance if one were to move strictly orthogonally,
        which is what the snake can do.
        This method is used by that coward Greedy to run away from the food so he can eat it later.
        What a scam!
        :param p1: The first point of type Pos.
        :param p2: The second point of type Pos.
        :return: The sum of Delta x and Delta y, of type integer.
        """
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def direction_to(self, adj_pos):
        """
        Returns the direction in which one must go to get to the other point.
        :param adj_pos: A position on the map of type Pos.
        :return: A direction of type Direc.
        """
        if self.__x == adj_pos.__x:
            diff = self.__y - adj_pos.__y
            if diff == 1:
                return Direc.LEFT
            elif diff == -1:
                return Direc.RIGHT
        elif self.__y == adj_pos.__y:
            diff = self.__x - adj_pos.__x
            if diff == 1:
                return Direc.UP
            elif diff == -1:
                return Direc.DOWN
        return Direc.NONE

    def adj(self, direction):
        """
        Returns the point in a given direction
        :param direction: A direction of type Direc.
        :return: A position on the map of type Pos.
        """
        if direction == Direc.LEFT:
            return Pos(self.__x, self.__y - 1)
        if direction == Direc.RIGHT:
            return Pos(self.__x, self.__y + 1)
        if direction == Direc.UP:
            return Pos(self.__x - 1, self.__y)
        if direction == Direc.DOWN:
            return Pos(self.__x + 1, self.__y)
        return None

    def all_adj(self):
        """
        Returns a list of all the adjacent points.
        This is done by iterating through all the enums of Direc
        (a.k.a Up Down Left Right) and appending the positions they refer to to a list.
        :return: A list with contents of type Pos.
        """
        adjacents = []
        for direc in Direc:
            if direc != Direc.NONE:
                adjacents.append(self.adj(direc))
        return adjacents

    @property
    def x(self):
        """
        I think I've already said this before, but we use properties so that it is explicit whether or not the
        variables are from within the class or accessed from outside the class.
        :return: The value of x. Remember, x starts from top and goes DOWN.
        """
        return self.__x

    @x.setter
    def x(self, val):
        self.__x = val

    @property
    def y(self):
        """
        :return: The value of y. Remember, y starts from left and goes RIGHT.
        """
        return self.__y

    @y.setter
    def y(self, val):
        self.__y = val
