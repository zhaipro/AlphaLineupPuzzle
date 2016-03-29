# coding: utf-8
import numpy as np

from lineup_puzzle import Block
from lineup_puzzle import GameState
import mcts


np.random.seed(42)

Block.init()
gs = GameState.create()

print gs
while True:
    move, score = mcts.search(gs, 2)
    if move is None:
        break
    gs.move(*move)
    print move, score, gs.score
    print gs
