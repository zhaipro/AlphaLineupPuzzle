# coding: utf-8
import numpy as np

from AlphaLineupPuzzle import lineup_puzzle


# 棋盘当前位置是否有子
def get_board(gs):
    board = gs.board
    ones = np.ones_like(board)
    return board, ones - board


# 候选项
def get_alternative(gs):
    blocks = len(lineup_puzzle.Block.blocks)
    f = np.zeros(blocks)
    f[gs.alternative] = 1
    return f,


def state_to_tensor(gs):
    feat_tensors = []

    feat_tensors.extend(get_board(gs))
    feat_tensors.extend(get_alternative(gs))

    feat_tensors = [f.flatten() for f in feat_tensors]
    return np.concatenate(feat_tensors)


state_to_tensor.features = 2 * 7 * 7 + len(lineup_puzzle.Block.blocks)


def action_to_tensor(gs, idx, (x, y), size=7):
    idx = gs.alternative[idx]
    return np.array((x * 7 + y) * len(lineup_puzzle.Block.blocks) + idx)


action_to_tensor.features = 7 * 7 * len(lineup_puzzle.Block.blocks)
