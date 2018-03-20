# coding=utf-8
"""
Definitions for PathSolver class, which is the path-finder for Greedy and Hamilton..
Exported methods in PathSolver are longest path to tail and shortest path to food.
"""
import random
import sys
from collections import deque

from snake.map import PointType, Direc
from snake.solver.base import BaseSolver


class _TableCell:
    def __init__(self):
        self.reset()

    def __str__(self):
        return '{dist: {}  parent:{} visit:{}}'.format(self.dist, str(self.parent), self.visit)

    __repr__ = __str__

    def reset(self):
        """
        Reset the table cell.
        :return:
        """
        self.parent = None
        self.dist = sys.maxsize

        self.visit = False


class PathSolver(BaseSolver):
    """
    This is a helper class that contains two important algorithms:
    1. Shortest path from the head to a certain point.
    2. Longest path from the head to a certain point.
    Each of the solvers contains a PathSolver which helps compute the tedious tasks, which the solvers then interpret.
    """

    def __init__(self, snake):
        super().__init__(snake)
        self.__table = [[_TableCell() for _ in range(snake.map.num_cols)] for _ in range(snake.map.num_rows)]

    @property
    def table(self):
        """
        :return: Table. Used for Hamiltonian Cycle.
        """
        return self.__table

    def shortest_path_to_food(self):
        """
        :return: A deque of directions to go in to get the shortest path to food.
        """
        return self.path_to(self.map.food, 'shortest')

    def longest_path_to_tail(self):
        """
        :return: A deque of directions to go in to get the longest path to the tail.
        Used for hamiltonian cycle and greedy snake running away.
        """
        return self.path_to(self.snake.tail(), 'longest')

    def path_to(self, des, path_type):
        """
        This is a helper function that temporarily sets the point of the destination to empty.
        This is done so that it will be considered by the path_finding_algorithms, which only add points to the queue
        if they are empty.
        :param des: The destination of the path of type Pos.
        :param path_type: Either shortest or longest. Switches between method shortest_path_to and longest_path_to.
        :return: A deque of directions. Each direction is an enum Direc.
        """
        original_type = self.map.point(des).type
        self.map.point(des).type = PointType.EMPTY
        path = deque()
        if path_type == 'shortest':
            path = self.shortest_path_to(des)
        elif path_type == 'longest':
            path = self.longest_path_to(des)
        self.map.point(des).type = original_type
        return path

    def shortest_path_to(self, des):
        """
        Find the shortest path from the snake's head to the destination.
        This is a BFS implementation for snake.
        :param des: The destination position on the map of type Pos.
        :return: A deque of instructions(directions) for the snake.
        """
        self.__reset_table()
        head = self.snake.head()
        self.__table[head.x][head.y].dist = 0
        queue = deque()
        queue.append(head)
        while queue:
            cur = queue.popleft()
            if cur == des:
                return self.__build_path(head, des)
            if cur == head:
                first_direc = self.snake.direc
            else:
                first_direc = self.__table[cur.x][cur.y].parent.direction_to(cur)
            adjacents = cur.all_adj()
            random.shuffle(adjacents)
            # Arrange the order of traverse to make the path as straight as possible.
            for i, pos in enumerate(adjacents):
                if first_direc == cur.direction_to(pos):
                    adjacents[0], adjacents[i] = adjacents[i], adjacents[0]
                    break
            for pos in adjacents:
                if self.__is_valid(pos):
                    adj_cell = self.__table[pos.x][pos.y]
                    if adj_cell.dist == sys.maxsize:  # If it hasn't been visited yet
                        adj_cell.parent = cur
                        adj_cell.dist = self.__table[cur.x][cur.y].dist + 1
                        queue.append(pos)
        return deque()

    def longest_path_to(self, des):
        """
        Find the longest path from the snake's head to the destination.
        This is done by getting the shortest path,
        then extending the path by pushing it out.
        :param des: THe destination position on the map of type Pos.
        :return: A deque of instructions(directions) for the snake.
        """
        path = self.shortest_path_to(des)
        if not path:  # If you can't even get there, then return an empty deque.
            return deque()
        self.__reset_table()  # Ensure idempotency.
        cur = head = self.snake.head()
        # Set all positions on the shortest path to visited.
        self.__table[cur.x][cur.y].visit = True
        for direc in path:
            cur = cur.adj(direc)
            self.__table[cur.x][cur.y].visit = True
        idx, cur = 0, head
        while True:
            cur_direc = path[idx]
            nxt = cur.adj(cur_direc)
            tests = []
            # We create a next because we need to push out two "blocks" at once.
            # How this works is the algorithm checks two adjacent points,
            # and sees if they can be pushed out in the opposite direction.
            if cur_direc == Direc.LEFT or cur_direc == Direc.RIGHT:
                tests = [Direc.UP, Direc.DOWN]
                # Then we can try extending the path up or down.
            elif cur_direc == Direc.UP or cur_direc == Direc.DOWN:
                tests = [Direc.LEFT, Direc.RIGHT]
                # If the direction is moving up, then we try pushing it out sideways..
            extended = False
            for test_direc in tests:
                cur_test = cur.adj(test_direc)
                nxt_test = nxt.adj(test_direc)
                if self.__is_valid(cur_test) and self.__is_valid(nxt_test):
                    self.__table[cur_test.x][cur_test.y].visit = True
                    self.__table[nxt_test.x][nxt_test.y].visit = True
                    path.insert(idx, test_direc)  # We will insert that anti-shortcut into the path.
                    path.insert(idx + 2, Direc.opposite(test_direc))  # What goes out must eventually come back.
                    extended = True  # This tells the algorithm to continue checking that same point.
                    break
            if not extended:  # If there was no pushing out the path, then continue to the next point.
                cur = nxt
                idx += 1
                if idx >= len(path):
                    # Once all points have been checked, then break out of the loop and return the path.
                    break
        return path

    def __reset_table(self):
        """
        Reset the table for a new round of testing.
        This is done by calling the reset function for each cell,
        which deletes their parents (shocking, I know), and sets their visit to false.
        :return: Void.
        """
        for row in self.__table:
            for col in row:
                col.reset()

    def __build_path(self, src, des):
        """
        Build a path from the source from the destination, using the records of parent.
        :param src: The starting point. Usually the snake's head.
        :param des: The destination. Usually the food for Greedy,
        and the snake's tail for Hamiltonian Cycle.
        :return: A path of deque, tracing the path to get there. Each item in the deque is a Direc.
        """
        path = deque()
        tmp = des
        while tmp != src:
            parent = self.__table[tmp.x][tmp.y].parent
            path.appendleft(parent.direction_to(tmp))
            tmp = parent
        return path

    def __is_valid(self, pos):
        """
        This function checks if that point is valid.
        The two conditions that it checks is if the point has been visited before,
        and if it is safe, aka within the boundaries of the map and not a snake body.
        :param pos: A position of type Pos.
        :return: A boolean value, depending on if that position is valid or not.
        """
        return not self.__table[pos.x][pos.y].visit and self.map.is_safe(pos)
