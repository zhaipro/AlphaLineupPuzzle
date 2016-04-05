# coding: utf-8
import numpy as np

from AlphaLineupPuzzle import lineup_puzzle


def int_to_onehot(digit, max_value):
    oh = np.zeros(max_value)
    oh[digit] = 1
    return oh


def state_to_tensor(gs):
    blocks = len(lineup_puzzle.Block.blocks)
    feat_tensors = [int_to_onehot(idx, blocks) for idx in gs.alternative]
    feat_tensors.append(gs.board.reshape(gs.board.size))
    return np.concatenate(feat_tensors)


def action_to_tensor(idx, (x, y), size=7):
    oh = np.zeros((size, size, 3))
    oh[x, y, idx] = 1
    return oh.reshape(oh.size)
