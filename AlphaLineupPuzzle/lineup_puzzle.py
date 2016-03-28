# coding: utf-8
import itertools

import numpy as np


class Block(object):

    blocks = []

    def __init__(self, block):
        self.block = block

    def __eq__(self, other):
        return self.block.shape == other.block.shape and \
            np.all(self.block == other.block)

    @staticmethod
    def _add(block):
        b = Block(block)
        if b not in Block.blocks:
            Block.blocks.append(b)

    @staticmethod
    def add(block):
        block = np.array(block)
        Block._add(block)
        for _ in range(3):
            block = np.rot90(block)
            Block._add(block)

        block = np.fliplr(block)
        Block._add(block)
        for _ in range(3):
            block = np.rot90(block)
            Block._add(block)

    @staticmethod
    def init():
        Block.add([[1, 1, 0], [0, 1, 1]])    # z 4
        Block.add([[1], [1], [1], [1]])      # l 2
        Block.add([[1, 0], [1, 0], [1, 1]])  # L 8
        Block.add([[1, 1, 1], [0, 1, 0]])    # T 4
        Block.add([[1, 1], [1, 1]])          # # 1


class GameState(object):

    def __init__(self, size=7):
        self.size = size
        self.board = np.zeros((size, size))
        self.alternative = np.random.choice(Block.blocks, 3)

    def move(self, block, pos):
        if self.is_legal_move(block, pos):
            x, y = pos
            w, h = block.block.shape
            self.board[x:x + w, y:y + h] = block.block
        else:
            raise IllegalMove('illegal move pos: (%s, %s)' % pos)

    def legal_moves(self):
        t = range(self.size)
        for block, x, y in itertools.product(self.alternative, t, t):
            if self.is_legal_move(block, (x, y)):
                yield block, (x, y)

    def is_legal_move(self, block, pos):
        x, y = pos
        w, h = block.block.shape
        return 0 <= x <= self.size - w and 0 <= y <= self.size - h and \
            np.all(self.board[x:x + w, y:y + h] == 0)


class IllegalMove(Exception):
    pass
