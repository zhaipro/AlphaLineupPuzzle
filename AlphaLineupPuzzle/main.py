# coding: utf-8
from lineup_puzzle import Block
from lineup_puzzle import GameState
import mcts

Block.init()
gs = GameState()

print gs
while True:
    move, score = mcts.search(gs, 2)
    if move is None:
        break
    gs.move(*move)
    print move, score, gs.score
    print gs
