# coding=utf-8
"""
Tests for class Direc.
Tests to verify if getting the opposite direction works.
"""
from unittest import TestCase

from snake.map import Direc


class TestDirec(TestCase):
    def test_opposite(self):
        assert Direc.opposite(Direc.UP) == Direc.DOWN
        assert Direc.opposite(Direc.DOWN) == Direc.UP
        assert Direc.opposite(Direc.LEFT) == Direc.RIGHT
        assert Direc.opposite(Direc.RIGHT) == Direc.LEFT
