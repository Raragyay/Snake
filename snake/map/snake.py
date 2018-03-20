# coding=utf-8
"""Definition of class Snake. He will become the all-powerful."""
import random
from collections import deque

from snake.map.direction import Direc
from snake.map.point import PointType
from snake.map.pos import Pos


class Snake:
    """
    Definitions for snake object. This is the ancestor of all snakes.
    """

    def __init__(self, m, init_direc=None, init_bodies=None, init_types=None):
        """
        Initialize a Snake object.
        :param m: An object of type Map. Comes from snake.map.map.
        :param init_direc: Initial Direction for the snake of type Direc.
        :param init_bodies: Initial snake body positions. A list with contents of Pos.
        :param init_types: Types of each body in init_bodies. For drawing purposes. A list with contents of PointType.
        """
        self.__map = m
        self.__init_direc = init_direc
        self.__init_bodies = init_bodies
        self.__init_types = init_types
        self.reset(False)  # This randomizes the snake's position when it is created.

    def reset(self, reset_map=True):
        """
        Resets the snake's starting position.
        First, if an initial direction has not been given, the snake is initiated at a random position.
        It is also given a random init_direc
        Second, the snake is reset and its direction is set to init_direc.
        Its deque of bodies are also initiated. It is a deque because this allows for easy popping and appending
        on both sides of the list, which is necessary for creating new heads and removing old tails. In with the new,
        out with the old.
        Finally, the PointTypes are transferred to the map, ready to be drawn.
        :param reset_map: This decides if the map is reset to be completely empty as well.
        Obviously, this is unnecessary the first time, since initiating the Snake means
        passing a map object, which means it must have already been randomized.
        :return: Void! My favourite colour.
        """
        rand_init = False
        if self.__init_direc is None:
            rand_init = True
            head_row = random.randrange(2, self.__map.num_rows - 2)
            # We start at 2 so that the starting snake (of length 2) can extend in any direction.
            head_col = random.randrange(2, self.__map.num_cols - 2)
            head = Pos(head_row, head_col)
            self.__init_direc = random.choice([Direc.LEFT, Direc.UP, Direc.RIGHT, Direc.DOWN])
            self.__init_bodies = [head, head.adj(Direc.opposite(self.__init_direc))]
            self.__init_types = []
            if self.__init_direc == Direc.LEFT:
                self.__init_types.append(PointType.HEAD_L)
            elif self.__init_direc == Direc.UP:
                self.__init_types.append(PointType.HEAD_U)
            elif self.__init_direc == Direc.RIGHT:
                self.__init_types.append(PointType.HEAD_R)
            elif self.__init_direc == Direc.DOWN:
                self.__init_types.append(PointType.HEAD_D)
            if self.__init_direc in [Direc.LEFT, Direc.RIGHT]:
                self.__init_types.append(PointType.BODY_HOR)
            elif self.__init_direc in [Direc.UP, Direc.DOWN]:
                self.__init_types.append(PointType.BODY_VER)
        self.__steps = 0
        self.__dead = False
        self.__direc = self.__init_direc
        self.__direc_next = Direc.NONE
        self.__bodies = deque(self.__init_bodies)

        if reset_map:
            self.__map.reset()
        for i, pos in enumerate(self.__init_bodies):
            self.__map.point(pos).type = self.__init_types[i]
        if rand_init:
            self.__init_direc = self.__init_bodies = self.__init_types = None
            # Reset all initial values, for restarting..

    def copy(self):
        """
        Creates a copy of the snake with the same map, bodies, etc.
        The direction is not None, because we don't want to reset the snake body.
        :return: Snake Copy, Map Copy
        """
        m_copy = self.__map.copy()
        s_copy = Snake(m_copy, Direc.NONE, [], [])
        s_copy.__steps = self.__steps
        s_copy.__dead = self.__dead
        s_copy.__direc = self.__direc
        s_copy.__direc_next = self.__direc_next
        s_copy.__bodies = deque(self.__bodies)
        return s_copy, m_copy

    @property
    def map(self):
        """
        :return: Map.
        """
        return self.__map

    @property
    def steps(self):
        """
        :return: Number of steps taken by snake.
        """
        return self.__steps

    @property
    def dead(self):
        """
        :return: Boolean value of whether or not the snake is dead.
        """
        return self.__dead

    @dead.setter
    def dead(self, val):
        self.dead = val

    @property
    def direc(self):
        """
        :return: The direction of the snake as an enum.
        """
        return self.__direc

    @property
    def direc_next(self):
        """
        :return: The next direction for the snake.
        """
        return self.__direc_next

    @direc_next.setter
    def direc_next(self, val):
        self.__direc_next = val

    @property
    def bodies(self):
        """
        :return: The body of the snake. A list with contents Pos.
        """
        return self.__bodies

    def len(self):
        """
        :return: The length of the snake. Integer presumably. Can we have a 2.5 length snake?
        """
        return len(self.__bodies)

    def head(self):
        """
        :return: The head of the snake, as an object of type Pos.
        """
        return None if not self.__bodies else self.__bodies[0]

    def tail(self):
        """
        :return: The tail of the snake, as an object of type Pos.
        """
        return None if not self.__bodies else self.__bodies[-1]

    def move_path(self, path):
        """
        :param path: A path of type deque. Used for unit tests.
        :return: Void. Just moves.
        """
        for p in path:
            self.move(p)

    def move(self, new_direc=None):
        """
        Moves the snake. in the specified direction
        :param new_direc: The new direction to move in.
        If there is no new direction to move in, then the snake follows its old direction.
        :return: Void.
        """
        if new_direc is not None:
            self.__direc_next = new_direc
        if self.__dead or self.__direc_next == Direc.NONE or self.map.is_full():
            return
        old_head_type, new_head_type = self.__new_types()
        self.__map.point(self.head()).type = old_head_type
        new_head = self.head().adj(self.__direc_next)
        self.__bodies.appendleft(new_head)
        if not self.__map.is_safe(new_head):
            self.__dead = True
        if self.__map.point(new_head).type == PointType.FOOD:
            self.__map.rm_food()
        else:
            self.__rm_tail()
        self.__map.point(new_head).type = new_head_type
        self.__direc = self.__direc_next
        self.__steps += 1

    def __rm_tail(self):
        """
        This removes the tail of the snake by setting the point to be PointType Empty,
        and popping the tail of the snake from the list of bodies.
        :return: Void.
        """
        self.__map.point(self.tail()).type = PointType.EMPTY
        self.__bodies.pop()

    def __new_types(self):
        """
        This method decides the appearance of the heads, by looking at the previous direction, and the new direction.
        :return: The PointType for the old head (now part of the body),
        and the new head (which is defined by the new direction).
        """
        old_head_type, new_head_type = None, None
        # Set picture for new head.
        if self.__direc_next == Direc.LEFT:
            new_head_type = PointType.HEAD_L
        elif self.__direc_next == Direc.UP:
            new_head_type = PointType.HEAD_U
        elif self.__direc_next == Direc.RIGHT:
            new_head_type = PointType.HEAD_R
        elif self.__direc_next == Direc.DOWN:
            new_head_type = PointType.HEAD_D
        # Set picture for old head.
        if (self.__direc == Direc.LEFT and self.__direc_next == Direc.LEFT) or \
                (self.__direc == Direc.RIGHT and self.__direc_next == Direc.RIGHT):
            old_head_type = PointType.BODY_HOR
        elif (self.__direc == Direc.UP and self.__direc_next == Direc.UP) or \
                (self.__direc == Direc.DOWN and self.__direc_next == Direc.DOWN):
            old_head_type = PointType.BODY_VER
        elif (self.__direc == Direc.RIGHT and self.__direc_next == Direc.UP) or \
                (self.__direc == Direc.DOWN and self.__direc_next == Direc.LEFT):
            old_head_type = PointType.BODY_LU
        elif (self.__direc == Direc.LEFT and self.__direc_next == Direc.UP) or \
                (self.__direc == Direc.DOWN and self.__direc_next == Direc.RIGHT):
            old_head_type = PointType.BODY_UR
        elif (self.__direc == Direc.LEFT and self.__direc_next == Direc.DOWN) or \
                (self.__direc == Direc.UP and self.__direc_next == Direc.RIGHT):
            old_head_type = PointType.BODY_RD
        elif (self.__direc == Direc.RIGHT and self.__direc_next == Direc.DOWN) or \
                (self.__direc == Direc.UP and self.__direc_next == Direc.LEFT):
            old_head_type = PointType.BODY_DL
        return old_head_type, new_head_type
