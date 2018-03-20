# coding=utf-8
"""
Unit tests for Snake class.
First test makes sure that the initiation of the Snake is as intended.
Second test makes sure that movement is as intended: Tail is popped off and new head is appended.
Eating should halt tail destruction.
Third test makes sure that copying the snake results in a different snake that has the same attribute values
as original snake.
Fourth test makes sure that killing the snake makes it dead.
"""
from unittest import TestCase

from snake.map import Map, Snake, Direc, Pos, PointType


class TestSnake(TestCase):
    def test_init(self):
        m = Map(5, 5)
        # Remember, a 5 by 5 map only has 9 points because
        # There are walls on the side.
        s = Snake(m, Direc.RIGHT,
                  [Pos(1, 3), Pos(1, 2), Pos(1, 1)],
                  [PointType.HEAD_R, PointType.BODY_HOR, PointType.BODY_HOR])
        assert not s.dead
        assert s.direc is Direc.RIGHT
        assert s.len() == 3
        assert s.head() == Pos(1, 3)
        assert s.bodies[1] == Pos(1, 2)
        assert s.tail() == Pos(1, 1)
        assert m.point(Pos(1, 1)).type == PointType.BODY_HOR
        assert m.point(Pos(1, 2)).type == PointType.BODY_HOR
        assert m.point(Pos(1, 3)).type == PointType.HEAD_R

    def test_move_eat(self):
        m = Map(5, 5)
        s = Snake(m, Direc.RIGHT,
                  [Pos(1, 2), Pos(1, 1)],
                  [PointType.HEAD_R, PointType.BODY_HOR])
        assert s.len() == 2
        m.create_food(Pos(1, 3))
        s.move(Direc.RIGHT)
        assert s.head() == Pos(1, 3) and s.tail() == Pos(1, 1)
        assert m.point(s.tail()).type == PointType.BODY_HOR
        assert m.point(Pos(1, 2)).type == PointType.BODY_HOR
        assert m.point(s.head()).type == PointType.HEAD_R
        s.move(Direc.DOWN)
        assert s.head() == Pos(2, 3) and s.tail() == Pos(1, 2)
        assert m.point(s.tail()).type == PointType.BODY_HOR
        assert m.point(Pos(1, 3)).type == PointType.BODY_DL
        assert m.point(s.head()).type == PointType.HEAD_D
        s.move(Direc.LEFT)
        assert s.head() == Pos(2, 2) and s.tail() == Pos(1, 3)
        assert m.point(s.tail()).type == PointType.BODY_DL
        assert m.point(Pos(2, 3)).type == PointType.BODY_LU
        assert m.point(s.head()).type == PointType.HEAD_L
        s.move(Direc.LEFT)
        assert s.head() == Pos(2, 1) and s.tail() == Pos(2, 3)
        assert m.point(s.tail()).type == PointType.BODY_LU
        assert m.point(Pos(2, 2)).type == PointType.BODY_HOR
        assert m.point(s.head()).type == PointType.HEAD_L
        s.move(Direc.DOWN)
        assert s.head() == Pos(3, 1) and s.tail() == Pos(2, 2)
        assert m.point(s.tail()).type == PointType.BODY_HOR
        assert m.point(Pos(2, 1)).type == PointType.BODY_RD
        assert m.point(s.head()).type == PointType.HEAD_D
        s.move(Direc.RIGHT)
        assert s.head() == Pos(3, 2) and s.tail() == Pos(2, 1)
        assert m.point(s.tail()).type == PointType.BODY_RD
        assert m.point(Pos(3, 1)).type == PointType.BODY_UR
        assert m.point(s.head()).type == PointType.HEAD_R
        s.move(Direc.RIGHT)
        assert s.head() == Pos(3, 3) and s.tail() == Pos(3, 1)
        assert m.point(s.tail()).type == PointType.BODY_UR
        assert m.point(Pos(3, 2)).type == PointType.BODY_HOR
        assert m.point(s.head()).type == PointType.HEAD_R
        s.move(Direc.UP)
        assert s.head() == Pos(2, 3) and s.tail() == Pos(3, 2)
        assert m.point(s.tail()).type == PointType.BODY_HOR
        assert m.point(Pos(3, 3)).type == PointType.BODY_LU
        assert m.point(s.head()).type == PointType.HEAD_U
        s.move(Direc.LEFT)
        assert s.head() == Pos(2, 2) and s.tail() == Pos(3, 3)
        assert m.point(s.tail()).type == PointType.BODY_LU
        assert m.point(Pos(2, 3)).type == PointType.BODY_DL
        assert m.point(s.head()).type == PointType.HEAD_L
        s.move(Direc.LEFT)
        assert s.head() == Pos(2, 1) and s.tail() == Pos(2, 3)
        assert m.point(s.tail()).type == PointType.BODY_DL
        assert m.point(Pos(2, 2)).type == PointType.BODY_HOR
        assert m.point(s.head()).type == PointType.HEAD_L
        s.move(Direc.UP)
        assert s.head() == Pos(1, 1) and s.tail() == Pos(2, 2)
        assert m.point(s.tail()).type == PointType.BODY_HOR
        assert m.point(Pos(2, 1)).type == PointType.BODY_UR
        assert m.point(s.head()).type == PointType.HEAD_U
        s.move(Direc.RIGHT)
        assert s.head() == Pos(1, 2) and s.tail() == Pos(2, 1)
        assert m.point(s.tail()).type == PointType.BODY_UR
        assert m.point(Pos(1, 1)).type == PointType.BODY_RD
        assert m.point(s.head()).type == PointType.HEAD_R
        s.move(Direc.RIGHT)
        assert s.head() == Pos(1, 3) and s.tail() == Pos(1, 1)
        assert m.point(s.tail()).type == PointType.BODY_RD
        assert m.point(Pos(1, 2)).type == PointType.BODY_HOR
        assert m.point(s.head()).type == PointType.HEAD_R
        s.move(Direc.DOWN)
        s.move(Direc.DOWN)
        assert s.head() == Pos(3, 3) and s.tail() == Pos(1, 3)
        assert m.point(s.tail()).type == PointType.BODY_DL
        assert m.point(Pos(2, 3)).type == PointType.BODY_VER
        assert m.point(s.head()).type == PointType.HEAD_D
        s.move(Direc.LEFT)
        s.move(Direc.LEFT)
        s.move(Direc.UP)
        s.move(Direc.UP)
        assert s.head() == Pos(1, 1) and s.tail() == Pos(3, 1)
        assert m.point(s.tail()).type == PointType.BODY_UR
        assert m.point(Pos(2, 1)).type == PointType.BODY_VER
        assert m.point(s.head()).type == PointType.HEAD_U
        # Now that the snake has moved all around, let's make sure our snake hasn't died of exhaustion!
        assert s.len() == 3
        # Now let's stuff it with food.
        assert not m.is_full()
        food_pos = [
            Pos(1, 2),
            Pos(1, 3),
            Pos(2, 3),
            Pos(3, 3),
            Pos(3, 2),
            Pos(2, 2)
        ]
        move_direc = [
            Direc.RIGHT,
            Direc.RIGHT,
            Direc.DOWN,
            Direc.DOWN,
            Direc.LEFT,
            Direc.UP
        ]
        for i, pos in enumerate(food_pos):
            m.create_food(pos)
            s.move(move_direc[i])
        # Yum Yum! That must be really filling.
        assert m.is_full()
        assert s.len() == 9 and s.steps == 25 and not s.dead

    def test_copy(self):
        m = Map(5, 5)
        s = Snake(m, Direc.RIGHT,
                  [Pos(1, 3), Pos(1, 2), Pos(1, 1)],
                  [PointType.HEAD_R, PointType.BODY_HOR, PointType.BODY_HOR])
        s.move(Direc.DOWN)
        s.move(Direc.LEFT)
        s_copy, _ = s.copy()  # There's an underscore because it returns a map as well.
        assert id(s) != id(s_copy)
        assert s.steps == 2 and s.steps == s_copy.steps
        assert not s.dead and s.dead == s_copy.dead
        assert s.direc == Direc.LEFT and s.direc == s_copy.direc
        assert s.direc_next == Direc.LEFT and s.direc == s_copy.direc_next
        for idx, body in enumerate(s.bodies):
            assert body == s_copy.bodies[idx]

    def test_dead(self):
        m = Map(5, 5)
        s = Snake(m, Direc.RIGHT,
                  [Pos(1, 3), Pos(1, 2), Pos(1, 1)],
                  [PointType.HEAD_R, PointType.BODY_HOR, PointType.BODY_HOR])
        assert not s.dead
        s.move(s.direc)
        assert s.dead and s.len() == 3 and s.head() == Pos(1, 4)

        m.reset()
        s = Snake(m, Direc.RIGHT,
                  [Pos(1, 3), Pos(1, 2), Pos(1, 1)],
                  [PointType.HEAD_R, PointType.BODY_HOR, PointType.BODY_HOR])
        assert not s.dead  # Testing for idempotency. I like that word now.
        s.move(Direc.UP)
        assert s.dead and s.len() == 3 and s.head() == Pos(0, 3)

        m.reset()
        s = Snake(m, Direc.DOWN,
                  [Pos(3, 1), Pos(2, 1), Pos(1, 1)],
                  [PointType.HEAD_D, PointType.BODY_VER, PointType.BODY_VER])
        assert not s.dead
        s.move(s.direc)
        assert s.dead and s.len() == 3 and s.head() == Pos(4, 1)

        m.reset()
        s = Snake(m, Direc.DOWN,
                  [Pos(3, 1), Pos(2, 1), Pos(1, 1)],
                  [PointType.HEAD_D, PointType.BODY_VER, PointType.BODY_VER])
        assert not s.dead
        s.move(Direc.LEFT)
        assert s.dead and s.len() == 3 and s.head() == Pos(3, 0)

        # We've banged our snake into the wall from every direction possible.
        # Now let's make it bang into itself.
        m.reset()
        s = Snake(m, Direc.LEFT,
                  [Pos(2, 2), Pos(1, 2), Pos(1, 1), Pos(2, 1), Pos(3, 1)],
                  [PointType.HEAD_D, PointType.BODY_DL, PointType.BODY_RD, PointType.BODY_VER, PointType.BODY_VER])
        assert not s.dead
        s.move(s.direc)
        assert s.dead and s.len() == 5 and s.head() == Pos(2, 1)
