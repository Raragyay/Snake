# coding=utf-8
"""
Tests for the Map class.
We test if the creation of a map class is as expected.
"""
from unittest import TestCase

import pytest

from snake.map import Map, PointType, Pos


class TestMap(TestCase):
    def test_init(self):
        with pytest.raises(TypeError):
            _ = Map(5, 1.5)
        with pytest.raises(ValueError):
            _ = Map(4, 5)
        m = Map(12, 12)
        for i in range(m.num_rows):
            for j in range(m.num_cols):
                if i == 0 or i == m.num_rows - 1 or j == 0 or j == m.num_cols - 1:
                    assert m.point(Pos(i, j)).type == PointType.WALL
                else:
                    assert m.point(Pos(i, j)).type == PointType.EMPTY
