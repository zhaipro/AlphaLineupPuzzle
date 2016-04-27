# coding: utf-8
import unittest

import numpy as np

from AlphaLineupPuzzle import util


class TestUtil(unittest.TestCase):

    def test_augment_array(self):
        origin = [[1, 0], [1, 0], [1, 1]]    # L型块，有八种不同的增广
        augments = []
        for block in util.augment(origin):
            # 与之前增广出来的都不一样
            for a in augments:
                ret = np.array_equal(a, block)
                self.assertFalse(ret)
            augments.append(block)
        # 共八种
        self.assertEqual(len(augments), 8)

    def test_augment_pos(self):
        augments = [(1, 2), (2, 1), (4, 2), (2, 4),
                    (2, 1), (4, 2), (2, 4), (1, 2)]
        self.assertListEqual(list(util.augment_pos(augments[0], 7, (2, 3))), augments)

    def test_(self):
        pos = (1, 2)
        size = 7
        board = np.zeros((size, size))
        board[pos] = 1
        # 数组的增广顺序与位置增广顺序相同。
        for board, pos in zip(util.augment(board), util.augment_pos(pos, size, (1, 1))):
            self.assertEqual(board[pos], 1)
