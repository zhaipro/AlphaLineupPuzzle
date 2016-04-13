# coding: utf-8
'''
全程硬编码，0表示指定位置没有方块，1表示有方块
'''
import itertools

import numpy as np


class Block(object):

    blocks = []
    base = {}

    def __init__(self, block):
        self.block = block

    def __eq__(self, other):
        return np.array_equal(self.block, other.block)

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
        '''
        添加形状block以及它的所有变体（旋转、镜面）
        '''
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
    def create(size=7, alternative=None):
        gs = GameState()
        gs.score = 0
        gs.size = size
        gs.board = np.zeros((size, size), dtype=np.int)
        if alternative:
            assert len(alternative) == 3, '只能有三个候选项'
            gs.alternative = list(alternative)
        else:
            gs.alternative = np.random.randint(0, len(Block.blocks), 3)

        # l记录游戏进程
        # 格式如：[((idx, (x, y)), next)]
        # 其中:
        #     idx表示某次玩家从候选列表中选择的方块(0~2)
        #     (x, y)表示放置位置
        #     表示玩家选择后棋盘随机产生的下一个方块编号
        gs.history = [tuple(gs.alternative)]   # 游戏历史

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
        block_idx = self.alternative[idx]
        block = Block.blocks[block_idx]
        self._move(block, pos)
        block_idx = np.random.randint(0, len(Block.blocks))
        self.alternative[idx] = block_idx
        if self.history:
            self.history.append(((idx, pos), block_idx))

    def legal_moves(self):
        t = range(self.size)
        for (idx, block_idx), x, y in itertools.product(enumerate(self.alternative), t, t):
            block = Block.blocks[block_idx]
            if self.is_legal_move(block, (x, y)):
                yield idx, (x, y)

    def is_legal_move(self, block, pos):
        x, y = pos
        w, h = block.block.shape
        return 0 <= x <= self.size - w and 0 <= y <= self.size - h and \
            not np.sum(self.board[x:x + w, y:y + h] * block.block)
        # not np.any(self.board[x:x + w, y:y + h] * block.block)
        # np.all(self.board[x:x + w, y:y + h] * block.block == 0)

    def update(self):
        a = self.board.sum(0)   # 竖着
        b = self.board.sum(1)   # 横着

        self.board[:, a == self.size] = 0
        self.score += ((a == self.size) * 500).sum()

        self.board[b == self.size] = 0
        self.score += ((b == self.size) * 500).sum()

    def copy(self):
        gs = GameState()
        gs.size = self.size
        gs.score = self.score
        gs.board = self.board.copy()
        gs.alternative = self.alternative.copy()
        gs.history = None
        return gs

    def ext(self, idx):
        for block_idx, _ in enumerate(Block.blocks):
            gs = self.copy()
            gs.alternative[idx] = block_idx
            yield gs

    def __str__(self):
        s = ['=' * 10, str(self.board), ]
        for idx in self.alternative:
            s.append(str(Block.blocks[idx]))
        s.append('-' * 10)
        return '\n'.join(s)


class IllegalMove(Exception):
    pass
