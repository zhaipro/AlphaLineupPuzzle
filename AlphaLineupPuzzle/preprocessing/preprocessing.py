# coding: utf-8
import numpy as np

from AlphaLineupPuzzle import lineup_puzzle


def int_to_onehot(digit, max_value):
    oh = np.zeros(max_value)
    oh[digit] = 1
    return oh


def state_to_tensor(gs):
    # 候选项
    blocks = len(lineup_puzzle.Block.blocks)
    feat_tensors = [int_to_onehot(idx, blocks) for idx in gs.alternative]
    # 棋盘当前位置是否有子
    feat_tensors.append(gs.board.reshape(gs.board.size))
    # 棋盘当前位置可放置哪些候选项
    f = np.zeros((3, gs.size, gs.size))
    for idx, (x, y) in gs.legal_moves():
        f[idx, x, y] = 1
    feat_tensors.append(f.reshape(f.size))
    return np.concatenate(feat_tensors)


state_to_tensor.features = len(lineup_puzzle.Block.blocks) * 3 + 4 * 7 * 7


def action_to_tensor(idx, (x, y), size=7):
    return np.array((x * 7 + y) * 3 + idx)


action_to_tensor.features = 3 * 7 * 7
