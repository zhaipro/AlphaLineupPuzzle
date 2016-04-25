# coding: utf-8
import unittest

import numpy as np

from AlphaLineupPuzzle.models import policy


class TestPolicy(unittest.TestCase):

    def test_(self):
        model = policy.Policy(100, 20)
        model.forward(np.random.random((2, 100)))
