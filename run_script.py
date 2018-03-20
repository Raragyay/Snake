# coding=utf-8
"""
Main run script.
Comment out GreedySolver to get a 100% success rate.
Comment out HamiltonSolver to get a fun snake that's very greedy.
"""
from snake.game import GameConfig, Game

conf = GameConfig()
# conf.solver_name = 'HamiltonSolver'
conf.solver_name = 'GreedySolver'
Game(conf).run()
