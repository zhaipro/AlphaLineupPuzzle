# coding: utf-8
import numpy as np

from lineup_puzzle import Block
from lineup_puzzle import GameState
import mcts


np.random.seed(42)

Block.init()
gs = GameState.create()

gs = GameState.create()
while True:
    print gs
    action, value = mcts.get_move(gs)
    if action is None:
        break
    gs.move(*action)
    print action, value, gs.score, value - gs.score
