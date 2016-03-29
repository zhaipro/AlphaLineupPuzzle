# coding: utf-8
import itertools

import numpy as np


class Block(object):

    blocks = []
    base = {}

    def __init__(self, block):
        self.block = block

    def __eq__(self, other):
        return self.block.shape == other.block.shape and \
            np.all(self.block == other.block)

    def __str__(self):
        return str(self.block)

    @staticmethod
    def _add(block):
        b = Block(block)
        if b not in Block.blocks:
            Block.blocks.append(b)
        return b

    @staticmethod
    def add(block, name):
        block = np.array(block)
        b = Block._add(block)
        Block.base[name] = b
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
        Block.add([[1, 1, 0], [0, 1, 1]], 'z')    # z 4
        Block.add([[1], [1], [1], [1]], 'l')      # l 2
        Block.add([[1, 0], [1, 0], [1, 1]], 'L')  # L 8
        Block.add([[1, 1, 1], [0, 1, 0]], 'T')    # T 4
        Block.add([[1, 1], [1, 1]], '#')          # # 1
        Block.blocks = np.array(Block.blocks)


class GameState(object):

    @staticmethod
    def create(size=7):
        gs = GameState()
        gs.score = 0
        gs.size = size
        gs.board = np.zeros((size, size), dtype=np.int)
        gs.alternative = np.random.choice(Block.blocks, 3)
        return gs

    def _move(self, block, pos):
        if self.is_legal_move(block, pos):
            x, y = pos
            w, h = block.block.shape
            self.board[x:x + w, y:y + h] += block.block
            self.update()
        else:
            raise IllegalMove('illegal move pos: (%s, %s)' % pos)

    def move(self, idx, pos):
        self._move(self.alternative[idx], pos)
        self.alternative[idx] = np.random.choice(Block.blocks)

    def legal_moves(self):
        t = range(self.size)
        for (idx, block), x, y in itertools.product(enumerate(self.alternative), t, t):
            if self.is_legal_move(block, (x, y)):
                yield idx, (x, y)

    def is_legal_move(self, block, pos):
        x, y = pos
        w, h = block.block.shape
        return 0 <= x <= self.size - w and 0 <= y <= self.size - h and \
            np.all((self.board[x:x + w, y:y + h] * block.block) == 0)

    def update(self):
        a = self.board.sum(0)   # 竖着
        self.board[:, a == self.size] = 0
        self.score += ((a == self.size) * 500).sum()

        a = self.board.sum(1)   # 横着
        self.board[a == self.size] = 0
        self.score += ((a == self.size) * 500).sum()

    def copy(self):
        gs = GameState()
        gs.size = self.size
        gs.score = self.score
        gs.board = self.board.copy()
        gs.alternative = self.alternative.copy()
        return gs

    def ext(self, idx):
        for block in Block.blocks:
            gs = self.copy()
            gs.alternative[idx] = block
            yield gs

    def __str__(self):
        s = ['=' * 10, str(self.board), ]
        for a in self.alternative:
            s.append(str(a))
        s.append('-' * 10)
        return '\n'.join(s)


class IllegalMove(Exception):
    pass
