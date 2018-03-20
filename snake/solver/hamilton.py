# coding=utf-8
"""Definitions for class Hamilton"""
from snake.map import Direc

from snake.solver import PathSolver
from snake.solver.base import BaseSolver


class _TableCell:
    """
    A table cell. It has some numbers on it,
    probably from when it was indoctrinated to act like a table cell as a child.
    """

    def __init__(self):
        self.reset()

    def __str__(self):
        return '{idx: {} direc: {}}'.format(self.idx, self.direc)

    __repr__ = __str__

    def reset(self):
        """
        Resets the table cell for further indoctrination.
        :return: Void. Of all emotions.
        """
        self.idx = None
        self.direc = Direc.NONE


class HamiltonSolver(BaseSolver):
    """
    A snake called Hamilton. It goes around in big, big circles.
    """

    def __init__(self, snake, shortcuts=True):
        if snake.map.num_rows % 2 != 0 or snake.map.num_cols % 2 != 0:
            raise ValueError('num_rows and num_cols must be even.')
        super().__init__(snake)
        self.__shortcuts = shortcuts
        self.__path_solver = PathSolver(snake)
        self.__table = [[_TableCell() for _ in range(snake.map.num_cols)] for _ in range(snake.map.num_rows)]
        self.__build_cycle()

    @property
    def table(self):
        """
        :return: The poor table cells, all bunched up and forced to be numbers and strings.
        """
        return self.__table

    def next_direc(self):
        """
        Gets the next direction, taking shortcuts if it won't disrupt the cycle.
        :return: The next direction to go in of type Direc.
        """
        head = self.snake.head()
        nxt_direc = self.__table[head.x][head.y].direc
        # We should take shortcuts if the snake isn't too long, to speed up gameplay.
        if self.__shortcuts and self.snake.len() < 0.5 * self.map.capacity:
            path = self.__path_solver.shortest_path_to_food()
            # Check if there is a path from the head to the food.
            if path:
                tail, nxt, food = self.snake.tail(), head.adj(path[0]), self.map.food
                tail_idx = self.__table[tail.x][tail.y].idx  # Get the location of the tail on the hamiltonian cycle.
                head_idx = self.__table[head.x][head.y].idx  # Get the location of the head on the hamiltonian cycle.
                nxt_idx = self.__table[nxt.x][nxt.y].idx
                # Get the location of the next move,
                # if Hamilton were to follow the shortest path to the food.
                food_idx = self.__table[food.x][food.y].idx  # Get the location of the food on the hamiltonian cycle.
                if not (len(path) == 1 and abs(food_idx - tail_idx) == 1):
                    # Make sure that either the path does not lead to instant death.
                    # This is because if it takes exactly one move to get to the food,
                    # and the tail is next on the hamiltonian cycle,
                    # the tail will "freeze" and so the head, which will continue to follow the hamiltonian cycle
                    # (remember, it does not have any self-preserving capabilities like the greedy solver),
                    # will smash the tail and will result in certain death.
                    head_idx_rel = self.__relative_dst(tail_idx, head_idx, self.map.capacity)
                    nxt_idx_rel = self.__relative_dst(tail_idx, nxt_idx, self.map.capacity)
                    food_idx_rel = self.__relative_dst(tail_idx, food_idx, self.map.capacity)
                    if head_idx_rel < nxt_idx_rel <= food_idx_rel:  # Average 1786.16 for 100 tests.
                        # if head_idx < nxt_idx <= food_idx:  # Fails quite often. Still trying to figure out why.
                        # If the next move suggested by the bfs solver would jump the head closer to the food,
                        # and wouldn't overshoot the food, then go ahead.
                        nxt_direc = path[0]
        return nxt_direc

    def __build_cycle(self):
        """
        Build a hamiltonian cycle on the map.
        0 is the head, and capacity of the map is the end of the cycle.
        :return: Void.
        """
        path = self.__path_solver.longest_path_to_tail()
        # The longest path to the tail, assuming that the map is square and even,
        # guarantees that the path will pass through every single point on the map.
        cur, cnt = self.snake.head(), 0
        for direc in path:
            self.__table[cur.x][cur.y].idx = cnt
            self.__table[cur.x][cur.y].direc = direc
            cur = cur.adj(direc)
            cnt += 1
        tail = self.snake.tail()
        self.__table[tail.x][tail.y].idx = cnt
        self.__table[tail.x][tail.y].direc = self.snake.direc
        # With this we have a cycle that's composed of the whole grid.
        # It might seem a little boring, but eh.

    @staticmethod
    def __relative_dst(tail, x, size):
        """
        Gets the distance from tail to x on the hamiltonian cycle.
        :param tail: The position of the tail on the hamiltonian cycle of type Integer.
        :param x: An index on the hamiltonian cycle of type integer.
        :param size: The length of the cycle. This is so that if the tail is ahead of x at some point,
                     we can establish the total number of steps needed to get from
                     tail to x following the hamiltonian cycle.
        :return: Relative distance from the tail to the location of type Integer.
        """
        if tail > x:
            x += size
        return x - tail
