# coding: utf-8
import unittest
import tempfile

from AlphaLineupPuzzle import lineup_puzzle
from AlphaLineupPuzzle.preprocessing import game_converter


class TestGameConverter(unittest.TestCase):

    def setUp(self):
        self.save = 'tests/data/save.json'
        self.gs = lineup_puzzle.GameState.create()

    def test_to_file(self):
        temp_fn = tempfile.mktemp('.json', 'AlphaLineupPuzzle')
        self.gs.move(0, (1, 2))
        game_converter.Save.dump(self.gs, temp_fn)

    def test_convert_game(self):
        for state, action in game_converter.convert_game(self.save):
            pass

    def test_convert_to_hdf5(self):
        output = 'tests/data/save.hdf5'
        game_converter.to_hdf5((self.save,), output)
        states, actions = game_converter.from_hdf5(output)
