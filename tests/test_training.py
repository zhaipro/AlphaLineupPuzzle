# coding: utf-8
import unittest

from AlphaLineupPuzzle.training import training
from AlphaLineupPuzzle.preprocessing import game_converter


class TestPolicy(unittest.TestCase):

    def test_(self):
        states, actions = game_converter.from_hdf5('tests/data/save.hdf5')
        training.training(states, actions)
