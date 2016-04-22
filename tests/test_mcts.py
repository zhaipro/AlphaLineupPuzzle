# coding: utf-8
import unittest

from AlphaLineupPuzzle import lineup_puzzle
from AlphaLineupPuzzle import mcts


class TestMcts(unittest.TestCase):

    def setUp(self):
        lineup_puzzle.Block.init()
        self.gs = lineup_puzzle.GameState.create()

    def test_(self):
        mcts.StateNode.get_move(self.gs, 2, 300)
