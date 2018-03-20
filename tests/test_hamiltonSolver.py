# coding=utf-8
"""
Tests for Mr. Hamilton himself.
This is done by testing if going through the whole cycle goes through the whole map.
"""
from unittest import TestCase

from snake.map import Map, Snake, Direc, Pos, PointType
from snake.solver import HamiltonSolver


class TestHamiltonSolver(TestCase):
    def test_cycle(self):
        m = Map(6, 6)
        s = Snake(m, Direc.RIGHT,
                  [Pos(1, 2), Pos(1, 1)],
                  [PointType.HEAD_R, PointType.BODY_HOR])
        solver = HamiltonSolver(s, False)
        # No shortcuts please.
        table = solver.table
        cnt = 0
        original_head = s.head()
        while True:
            head = s.head()
            assert cnt == table[head.x][head.y].idx
            s.move(solver.next_direc())
            cnt += 1
            if s.head() == original_head:
                break
        assert cnt == m.capacity
