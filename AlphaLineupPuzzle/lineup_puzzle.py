# coding: utf-8
'''
全程硬编码，0表示指定位置没有方块，1表示有方块
为了速度，该模块只支持尺寸小于等于7的棋盘

以棋盘左上角为原点，向下为x轴，向右为y轴
0x2表示棋盘最上一行，从左向右数第二个位置上有一个小块
'''
import itertools

import numpy as np

import util


class Block(object):

    blocks = []
    _blocks = []
    base = {}

    @staticmethod
    def create(block):
        b = 0
        for x, row in enumerate(block):
            for y, val in enumerate(row):
                if val:
                    b |= 1 << (8 * x + y)
        return b

    @staticmethod
    def to_str(block):
        s = ''
        count = 0
        while block:
            s += '#' if block & 1 else ' '
            block >>= 1
            count += 1
            if count % 8 == 0:
                s += '\n'
        return s

    @staticmethod
    def _add(block):
        b = Block.create(block)
        if b not in Block.blocks:
            Block.blocks.append(b)
            Block._blocks.append(block.copy())
        return b

    @staticmethod
    def add(block, name):
        '''
        添加形状block以及它的所有变体（旋转、镜面）
        '''
        for block in util.augment(block):
            b = Block._add(block)
            Block.base.setdefault(name, b)

    @staticmethod
    def augment(block_idx, idx):
        return Block.transforms[block_idx][idx]

    @staticmethod
    def init():
        Block.add([[1, 1, 0], [0, 1, 1]], 'z')    # z 4
        Block.add([[1], [1], [1], [1]], 'l')      # l 2
        Block.add([[1, 0], [1, 0], [1, 1]], 'L')  # L 8
        Block.add([[1, 1, 1], [0, 1, 0]], 'T')    # T 4
        Block.add([[1, 1], [1, 1]], '#')          # # 1
        # Block.blocks = np.array(Block.blocks, dtype=np.int64)

        def block2idx(b):
            # 数组到索引
            b = Block.create(b)
            idx = Block.blocks.index(b)
            return idx

        Block.transforms = [map(block2idx, util.augment(b)) for b in Block._blocks]


Block.init()    # 在模块内自行初始化


class GameState(object):
    '''
    全程默认棋盘中有三个候选项，
    可以设置大小也只是为了方便测试，正式环境全部是7 x 7
    '''

    @staticmethod
    def create(size=7, alternative=None):
        gs = GameState()
        gs.score = 0
        gs.size = size
        gs._board = 0xff80808080808080
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
        x, y = pos
        block = block << (8 * x + y)
        if self._is_legal_move(block):
            self._board |= block
            self.update()
        else:
            raise IllegalMove('illegal move: %x' % block)

    def move(self, idx, pos, next_alternative=None):
        block_idx = self.alternative[idx]
        block = Block.blocks[block_idx]
        self._move(block, pos)

        if next_alternative is None:
            next_alternative = np.random.randint(0, len(Block.blocks))
        self.alternative[idx] = next_alternative
        if self.history:
            self.history.append(((idx, pos), next_alternative))

    def legal_moves(self):
        t = range(self.size)
        for (idx, block_idx), x, y in itertools.product(enumerate(self.alternative), t, t):
            block = Block.blocks[block_idx]
            if self.is_legal_move(block, (x, y)):
                yield idx, (x, y)

    def _legal_moves(self):
        for idx, block_idx in enumerate(self.alternative):
            block = Block.blocks[block_idx]
            for _ in xrange(8 * self.size):
                if self._is_legal_move(block):
                    yield idx, block
                block <<= 1

    def _is_legal_move(self, block):
        return (self._board & block) == 0

    def is_legal_move(self, block, pos):
        x, y = pos
        block = block << (8 * x + y)
        return (self._board & block) == 0

    def update(self):
        clear = 0
        for mask, shift in ((0x7f, 8), (0x0001010101010101, 1)):
            for _ in xrange(self.size):
                if (self._board & mask) == mask:
                    self.score += 500
                    clear |= mask
                mask <<= shift
        self._board ^= clear

    def copy(self):
        gs = GameState()
        gs.size = self.size
        gs.score = self.score
        gs._board = self._board
        gs.alternative = self.alternative.copy()
        gs.history = None
        return gs

    def ext(self, idx):
        for block_idx, _ in enumerate(Block.blocks):
            gs = self.copy()
            gs.alternative[idx] = block_idx
            yield gs

    def __str__(self):
        s = ['=' * 10, Block.to_str(self._board), ]
        for idx in self.alternative:
            s.append('-' * 10)
            s.append(Block.to_str(Block.blocks[idx]))
        return '\n'.join(s)

    @property
    def board(self):
        baord = np.zeros((self.size, self.size))
        for pos in itertools.product(xrange(self.size), xrange(self.size)):
            if not self.is_legal_move(1, pos):
                baord[pos] = 1
        return baord


class IllegalMove(Exception):
    pass
