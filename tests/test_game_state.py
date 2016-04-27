# coding: utf-8
import unittest

import numpy as np

from AlphaLineupPuzzle.lineup_puzzle import GameState
from AlphaLineupPuzzle.lineup_puzzle import Block


class TestGameStat(unittest.TestCase):

    def setUp(self):
        self.gs = GameState.create()

    def test_blocks_len(self):
        self.assertEqual(len(Block.blocks), 19)

    def test_block_to_str(self):
        Block.to_str(Block.blocks[0])

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
        self.gs._move(Block.base['#'], (0, 1))
        self.gs._move(Block.base['L'], (0, 0))
        self.gs._move(Block.base['#'], (0, 3))
        self.gs._move(Block.base['#'], (1, 5))
        self.assertTrue((self.gs._board & 0x7f00) == 0)
        self.assertEqual(self.gs.score, 500)

    def test_update2(self):
        # 测试横竖连削
        self.gs._move(Block.base['#'], (0, 3))
        self.gs._move(Block.base['#'], (0, 5))
        self.gs._move(Block.base['L'], (2, 1))
        self.gs._move(Block.base['#'], (5, 0))
        self.gs._move(Block.base['T'], (0, 0))
        self.assertEqual(self.gs.score, 1000)

    def test_ext(self):
        for idx, _ in enumerate(self.gs.alternative):
            for _ in self.gs.ext(idx):
                pass

    def test_to_str(self):
        str(self.gs)
        self.gs.move(1, (0, 0))
        str(self.gs)

    def test_history(self):
        # 第一项为初始的三个候选项
        self.assertEqual(len(self.gs.history), 1)
        self.gs.move(1, (0, 0))
        self.assertEqual(len(self.gs.history), 2)
        # 第一步
        self.assertEqual(self.gs.history[1][0], (1, (0, 0)))
        self.assertTrue(0 <= self.gs.history[1][1] < len(Block.blocks))
        # 不对拷贝得来的游戏状态记录历史
        self.assertIsNone(self.gs.copy().history)

    def test_board(self):
        self.gs._move(Block.base['z'], (0, 0))
        board = np.zeros_like(self.gs.board)
        board[0, 0] = board[0, 1] = 1
        board[1, 1] = board[1, 2] = 1
        self.assertTrue(np.array_equal(self.gs.board, board))

    def test_transform(self):
        for idx, block_idxs in enumerate(Block.transforms):
            self.assertEqual(idx, block_idxs[0])
