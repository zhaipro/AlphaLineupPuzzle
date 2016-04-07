# coding: utf-8
import time
import numpy as np

from AlphaLineupPuzzle import lineup_puzzle


np.random.seed(42)
lineup_puzzle.Block.init()
gs = lineup_puzzle.GameState.create()
gs.move(0, (1, 2))
start = time.time()
for _ in xrange(5000):
    list(gs.legal_moves())
print time.time() - start
