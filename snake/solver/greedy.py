# coding=utf-8
"""
Definitions for GreedySolver.
This snake tries to get to the food whenever possible. There are 5 steps to this.
Step 1:     Get the shortest path to the food using BFS search. If that path exists, move to step 2.
            Otherwise, move to step 4.
Step 2:     Simulate a movement to that food. If it fills up the map, return that path. Otherwise, move to step 3.
Step 3:     After that simulated snake has "eaten" the food, calculate the longest path from the head to the tail.
            If the head can get to the tail in the simulated setting, then start moving along that path. Otherwise,
            move to Step 4.
Step 4:     This step is gone to if there is no path from the head to the food or if there is no path from the head
            to the tail after eating the food. In this case, we calculate the longest path from the head to the tail.
            This ensures that we begin making a full loop, and reevaluating to the food whenever it is available.
            If we can't even get to the tail, we're in some deep, deep trouble. To Step 5 we go!
Step 5:     At this point, we can only hope for miracles. Do you want to know what our greedy snake does? It RUNS AWAY!
            No, like literally, it chooses the path that is the furthest away from the snake, and goes that way.
"""
from snake.map import Pos
from snake.solver import PathSolver
from snake.solver.base import BaseSolver


class GreedySolver(BaseSolver):
    """    A greedy little snake that only seeks to eat food. smh.    """

    def __init__(self, snake):
        super().__init__(snake)
        self.__path_solver = PathSolver(snake)

    def next_direc(self):
        """
        Get the next direction to move in.
        :return: A direction of type Direc.
        """
        # Clone the snake.
        s_copy, m_copy = self.snake.copy()
        # Step 1: Get the path to the food. If path 1 exists, move to step 2.
        # Otherwise, move to step 4.
        self.__path_solver.snake = self.snake  # That's my snake you're looking at!
        path_to_food = self.__path_solver.shortest_path_to_food()
        if path_to_food:
            # Step 2: Make a virtual snake to eat the food along the path.
            s_copy.move_path(path_to_food)
            if m_copy.is_full():
                return path_to_food[0]
            # Step 3: Calculate the longest path from head to tail after eating food.
            # If that longest path exists, then move along that path.
            # Otherwise, go to step 4.
            self.__path_solver.snake = s_copy
            path_to_tail = self.__path_solver.longest_path_to_tail()
            if len(path_to_tail) > 1:
                return path_to_food[0]

        # Step 4: Calculate the longest path from head to tail.
        # Remember, there is no path to the food right now that will guarantee our survival.
        # Therefore, we do one full loop, and then check again.
        # If that path exists, then move along that path.
        # Else, move to step 5.
        self.__path_solver.snake = self.snake
        path_to_tail = self.__path_solver.longest_path_to_tail()
        if len(path_to_tail) > 1:
            return path_to_tail[0]

        # Step 5: RUN AWAY! No, seriously, get as far away as you can from the food.
        head = self.snake.head()
        direc, max_dist = self.snake.direc, -1
        for adj in head.all_adj():
            if self.map.is_safe(adj):
                dist = Pos.manhattan_distance(adj, self.map.food)
                if dist > max_dist:
                    max_dist = dist
                    direc = head.direction_to(adj)
        return direc
