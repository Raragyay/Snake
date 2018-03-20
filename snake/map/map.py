# coding=utf-8
""" Definition of class Map."""
import random

from snake.map.point import Point, PointType
from snake.map.pos import Pos


class Map:
    """
    Map is a 2d game map.
    X is the vertical (Yes, I know, it's weird, but bear with me, because rows are the first index in 2d arrays).
    It starts in the top left and increases as it goes down.
    Y is the horizontal(Yes, again, I know it's weird, but columns are the second [] in a 2d array).
    It starts in the top left and increases as it goes left.
    There are a couple key methods for map.

    First of all, the point method returns the point. This is important because it is passed to the food functions
    and for the is_safe, is_full and is_inside functions.
    These functions are used for pathfinding for Mr. Hamilton and the Greedy Snake. They ensure that the snake does not
    cross itself and that the snake dies when it's supposed to die.
    Food eating and creating is handled by the map as well. These functions are called by the snake.
    """

    def __init__(self, num_rows, num_cols):
        """
        :param num_rows: Integer of the number of rows, including walls. This is the x value.
        :param num_cols: Integer of the number of columns, including walls. This is the y value.
        """
        if not isinstance(num_cols, int) or not isinstance(num_rows, int):
            raise TypeError('\'num_rows\' and \'num_cols\' must be integers.')
        if num_rows < 5 or num_cols < 5:
            raise ValueError('\'num_rows\' and \'num_cols\' must be larger or equal to 5.')
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__capacity = (num_rows - 2) * (num_cols - 2)
        self.__content = [[Point() for _ in range(num_cols)] for _ in range(num_rows)]
        self.reset()

    def reset(self):
        """
        This resets the map, so that all points are empty,
        except for those points that are on the edge,
        which are walls.
        :return: Void.
        """
        self.__food = None
        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                if i == 0 or i == self.__num_rows - 1 or j == 0 or j == self.__num_cols - 1:
                    self.__content[i][j].type = PointType.WALL
                else:
                    self.__content[i][j].type = PointType.EMPTY

    def copy(self):
        """
        This literally copies the map into another map. What do you expect?
        But seriously, it creates a new map object with the exact same point values but
        with different memory locations and ids.
        :return: Void.
        """
        map_copy = Map(self.__num_rows, self.__num_cols)
        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                map_copy.__content[i][j].type = self.__content[i][j].type
        return map_copy

    def point(self, pos):
        """
        Returns a point on the map.

        DO NOT, I REPEAT DO NOT use this to assign new values for food,
        unless you're using the create_food method.

        This function is used to modify the point type when moving the snake.

        :param pos: An object of type Pos, which we use to get the point on the map.
        :return: A point in the map of type Point, whose type is an enum of PointType.
        """
        return self.__content[pos.x][pos.y]
        # See how much prettier it looks with pos.x and pos.y? Yay!

    def is_inside(self, pos):
        """
        Check if a point is inside the map boundaries.
        Used to check if the snake is dead and for path-finding in conjunction with is_empty.
        :param pos: An object of type Pos.
        :return: Boolean Value.
        """

        return 0 < pos.x < self.__num_rows - 1 and 0 < pos.y < self.__num_cols

    def is_empty(self, pos):
        """
        Check if the type of the point at a specific position is empty or not.
        :param pos: An object of type Pos, which we use to get the point on the map.
        :return: Boolean Value.
        """
        return self.is_inside(pos) and self.point(pos).type == PointType.EMPTY

    def is_safe(self, pos):
        """
        Check if the point is safe to go to, i.e. it is inside the bounds, and is either
        food or empty.
        :param pos: An object of type pos, which we use to get the point on the map.
        :return: Boolean Value.
        """
        return self.is_inside(pos) and (self.point(pos).type == PointType.EMPTY or
                                        self.point(pos).type == PointType.FOOD)

    def is_full(self):
        """
        Check if the map has been filled with the snake bodies. If it has, hooray!
        It's a success!
        This is done by checking if every point on the map is part of the snake, by virtue of the PointType Enum.
        :return: Boolean Value.
        """
        for i in range(1, self.__num_rows - 1):
            for j in range(1, self.__num_cols - 1):
                t = self.__content[i][j].type
                if t.value < PointType.HEAD_L.value:
                    return False
                    # We have the empty, wall, and food set to sub-100,
                    # so as long as it is sub 100, it's not snake!
        return True

    def has_food(self):
        """
        Checks if there is any food on the map.
        :return: Boolean Value.
        """
        return self.__food is not None

    def rm_food(self):
        """
        A function to eat food. Just kidding! You can't actually eat food.
        It just disappears and self.__food is None.
        :return: Void. Is that what they call it in Java?
        """
        if self.has_food():
            self.point(self.__food).type = PointType.EMPTY
            # Stop telling me that this is defined outside of the init function!
            self.__food = None

    def create_food(self, pos):
        """
        This creates a piece of food (I'm guessing it's an apple)
        at a specific location.
        This is done by setting the PointType at that location as Food,
        then giving the position of that food to the attribute __food.
        :param pos: An object of class Pos.
        :return: The glorious piece of food.
        """
        self.point(pos).type = PointType.FOOD
        self.__food = pos
        return self.__food

    def create_rand_food(self):
        """
        Creates a random piece of food at one of the empty spots.
        This is done by getting all the possible places where the food could be placed,
        then using random.choice to randomly choose a position.
        :return: None if there are no empty spots else the food in question.
        """
        possible_food_positions = []
        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                t = self.__content[i][j].type
                if t == PointType.EMPTY:
                    possible_food_positions.append(Pos(i, j))
                elif t == PointType.FOOD:
                    # Too much food! It'll make the snake bloat.
                    return None
        if possible_food_positions:
            return self.create_food(random.choice(possible_food_positions))
        else:
            return None

    @property
    def num_rows(self):
        """
        Returns the number of rows.
        We segregate the double underscore and the non-double underscore
        so that it looks nice and so that I can use these property thingies.
        Not really. I just searched it online.
        :return: The number of rows in the map.
        """
        return self.__num_rows

    @property
    def num_cols(self):
        """
        :return: The number of columns in the map.
        """
        return self.__num_cols

    @property
    def capacity(self):
        """
        :return: The capacity of the map, i.e., the size of the map minus the walls.
        """
        return self.__capacity

    @property
    def food(self):
        """
        :return: Oh wow! It's a piece of food. It returns the position of the food, of type Pos.
        """
        return self.__food
