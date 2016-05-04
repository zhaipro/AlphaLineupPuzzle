# coding: utf-8
import unittest

from AlphaLineupPuzzle import lineup_puzzle
from AlphaLineupPuzzle import models


class TestLoadModel(unittest.TestCase):

    def test_load(self):
        policy = models.load_policy_network('tests/data/v0.2')
        gs = lineup_puzzle.GameState.create()
        actions = policy(gs)
        self.assertAlmostEqual(sum(p for action, p in actions), 1, -3)
