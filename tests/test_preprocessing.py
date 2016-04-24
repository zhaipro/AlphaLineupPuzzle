# coding: utf-8
import unittest

import numpy as np

from AlphaLineupPuzzle import lineup_puzzle
from AlphaLineupPuzzle.preprocessing import preprocessing


class TestPreprocessing(unittest.TestCase):

    def test_int_to_onehot(self):
        oh = preprocessing.int_to_onehot(2, 4)
        ret = np.array_equal(oh, [0, 0, 1, 0])
        self.assertTrue(ret)

    def test_state_to_tensor(self):
        gs = lineup_puzzle.GameState.create()
        tensor = preprocessing.state_to_tensor(gs)

    def test_action_to_tensor(self):
        tensor = preprocessing.action_to_tensor(1, (1, 2))
        self.assertEqual(tensor, 28)
