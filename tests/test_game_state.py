# coding: utf-8
import unittest

import numpy as np

from AlphaLineupPuzzle.lineup_puzzle import GameState
from AlphaLineupPuzzle.lineup_puzzle import Block


class TestGameStat(unittest.TestCase):

    def setUp(self):
        Block.init()
        self.gs = GameState()

    def test_blocks_len(self):
        self.assertEqual(len(Block.blocks), 19)

    def test_move(self):
        self.gs.move(0, (0, 0))

    def test_is_legal_move(self):
        self.gs._move(Block.base['z'], (0, 0))
        ret = self.gs.is_legal_move(Block.base['#'], (0, 2))
        self.assertFalse(ret)
        ret = self.gs.is_legal_move(Block.base['T'], (0, 2))
        self.assertTrue(ret)

    def test_legal_moves(self):
        for idx, pos in self.gs.legal_moves():
            pass

    def test_update(self):
        self.gs._move(Block.base['T'], (0, 0))
        self.gs._move(Block.base['#'], (0, 3))
        self.gs._move(Block.base['#'], (0, 5))
        self.assertTrue(np.all(self.gs.board[0] == 0))
        self.assertEqual(self.gs.score, 500)

    def test_ext(self):
        for idx, _ in enumerate(self.gs.alternative):
            for _ in self.gs.ext(idx):
                pass
