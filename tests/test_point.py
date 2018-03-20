# coding=utf-8
"""
Tests for Point.
Tests for whether or not the default point type is empty,
and if changing the point type works properly.
"""
from unittest import TestCase

from snake.map import Point, PointType


class TestPoint(TestCase):
    def test_type(self):
        p = Point()
        assert p.type == PointType.EMPTY
        p.type = PointType.FOOD
        assert p.type == PointType.FOOD
