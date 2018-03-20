# coding=utf-8
"""
Test cases for Pos class.
We test that adjacents work. They are pretty important.
"""
from unittest import TestCase

from snake.map import Pos, Direc


class TestPos(TestCase):
    def test_init(self):
        p = Pos(-5, 5)
        assert p == Pos(-5, 5)
        p.x = -10
        p.y = 10
        assert p != Pos(-5, 5)
        assert p == Pos(-10, 10)

    def test_arithmetic(self):
        p1 = Pos(-5, 10)
        p2 = Pos(5, -10)
        p3 = p1 + p2
        p4 = p1 - p2
        p5 = p2 - p1
        assert p3 == Pos(0, 0)
        assert p3 - p1 == p2
        assert p3 - p2 == p1
        assert p4 == Pos(-10, 20)
        assert p5 == -Pos(-10, 20)
        assert p4 + p2 == p1
        assert p5 + p1 == p2

    def test_dist(self):
        p1 = Pos(-5, 20)
        p2 = Pos(10, 8)
        assert Pos.manhattan_distance(p1, p2) == 27

    def test_adj(self):
        p = Pos(0, 0)
        adjacents = p.all_adj()
        assert len(adjacents) == 4
        hit = [False] * 4
        assert hit.count(False) == 4
        for adj in adjacents:
            if adj == Pos(-1, 0):
                assert p.direction_to(adj) == Direc.UP
                hit[0] = True
            elif adj == Pos(1, 0):
                assert p.direction_to(adj) == Direc.DOWN
                hit[1] = True
            elif adj == Pos(0, 1):
                assert p.direction_to(adj) == Direc.RIGHT
                hit[2] = True
            elif adj == Pos(0, -1):
                assert p.direction_to(adj) == Direc.LEFT
                hit[3] = True
            else:
                raise ValueError("error adj Pos")
        assert hit.count(False) == 0
