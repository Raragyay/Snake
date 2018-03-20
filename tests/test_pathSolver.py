# coding=utf-8
"""
Tests for the path solver.
First test tests if the shortest path to food works as intended. The BFS should produce the same result every time.
Second test tests if the find_path removing the tail momentarily works, so that BFS can verify the shortest time.
It also tests to see if the longest path fills the whole map, which it should, given that either x or y are even.
Some proofs online, but I can't really understand them.
"""
from unittest import TestCase
from snake.map import Direc, Pos, PointType, Map, Snake
from snake.solver import PathSolver


class TestPathSolver(TestCase):
    def test_shortest_path_to_food(self):
        m = Map(7, 7)
        m.create_food(Pos(5, 5))
        s = Snake(m, Direc.RIGHT,
                  [Pos(2, 3), Pos(2, 2), Pos(2, 1)],
                  [PointType.HEAD_R, PointType.BODY_HOR, PointType.BODY_HOR])
        solver = PathSolver(s)
        # noinspection PyUnusedLocal
        act_path = solver.shortest_path_to_food()
        act_path = solver.shortest_path_to_food()  # Check idempotency
        # Idempotency is pretty much checking for side effects.
        # You're checking whether or not the algorithm will produce the same result if it is run multiple times.
        # We do this multiple times to verify that the table has been properly reset.
        expect_path = [
            Direc.RIGHT, Direc.RIGHT, Direc.DOWN, Direc.DOWN, Direc.DOWN
        ]
        assert len(act_path) == len(expect_path)
        for i, direc in enumerate(act_path):
            assert direc == expect_path[i]
        assert solver.table[5][1].dist == 5
        assert solver.table[5][1].dist == solver.table[5][5].dist
        # Empty path
        assert not solver.shortest_path_to(s.tail())

    def test_longest_path_to_tail(self):
        m = Map(6, 6)
        m.create_food(Pos(4, 4))
        s = Snake(m, Direc.RIGHT,
                  [Pos(1, 3), Pos(1, 2), Pos(1, 1)],
                  [PointType.HEAD_R, PointType.BODY_HOR, PointType.BODY_HOR])
        solver = PathSolver(s)
        # noinspection PyUnusedLocal
        act_path = solver.longest_path_to_tail()
        act_path = solver.longest_path_to_tail()  # Check idempotency
        expect_path = [
            Direc.RIGHT, Direc.DOWN, Direc.DOWN, Direc.DOWN, Direc.LEFT, Direc.LEFT, Direc.LEFT,
            Direc.UP, Direc.RIGHT, Direc.RIGHT, Direc.UP, Direc.LEFT, Direc.LEFT, Direc.UP
        ]
        assert m.point(s.tail()).type == PointType.BODY_HOR
        assert len(act_path) == len(expect_path)
        for i, direc in enumerate(act_path):
            assert direc == expect_path[i]
        # Empty path because the tail has not been 'emptied' yet,
        # so it is not a valid position to be added to the queue.
        # This means that after all the evaluations, None of them check the snake tail
        # Because it is not valid, according to the function, since
        # it is part of the body.
        # Therefore, we pass the path finders through a function called path_to
        # to remove the 'tail' at that location so it can be evaluated.
        assert not solver.longest_path_to(s.tail())
