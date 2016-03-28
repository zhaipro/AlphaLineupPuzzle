# coding: utf-8
import unittest

from AlphaLineupPuzzle import lineup_puzzle


class TestGameStat(unittest.TestCase):

    def setUp(self):
        lineup_puzzle.Block.init()
        self.gs = lineup_puzzle.GameState()

    def test_blocks_len(self):
        self.assertEqual(len(lineup_puzzle.Block.blocks), 19)

    def test_move(self):
        self.gs.move(lineup_puzzle.Block.blocks[0], (0, 0))

    def test_is_legal_move(self):
        self.gs.move(lineup_puzzle.Block.blocks[0], (0, 0))
        ret = self.gs.is_legal_move(lineup_puzzle.Block.blocks[0], (0, 0))
        self.assertEqual(ret, False)

    def test_legal_moves(self):
        for block, pos in self.gs.legal_moves():
            pass
