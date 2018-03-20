# coding=utf-8
""" Definitions for BaseSolver."""


class BaseSolver:
    """
    Super class of all the solvers.
    """

    def __init__(self, snake):
        self.__snake = snake
        self.__map = snake.map

    @property
    def map(self):
        """

        :return: Map.
        """
        return self.__map

    @property
    def snake(self):
        """

        :return: Snake.
        """
        return self.__snake

    @snake.setter
    def snake(self, val):
        self.__snake = val
        self.__map = val.map

    def next_direc(self):
        """
        Holder function.
        :return: None
        """
        return NotImplemented
