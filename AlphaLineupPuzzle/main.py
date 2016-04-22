# coding: utf-8
import argparse

import numpy as np

from lineup_puzzle import Block
from lineup_puzzle import GameState
import mcts
from preprocessing import game_converter


Block.init()


def play(verbose):
    gs = GameState.create()
    while True:
        if verbose:
            print gs
        action, value = mcts.get_move(gs)
        if action is None:
            break
        gs.move(*action)
        if verbose:
            print action, value, gs.score, value - gs.score
    return gs


def main(n, path, seed, verbose):
    if seed:
        np.random.seed(seed)

    for idx in xrange(n):
        gs = play(verbose)
        if path:
            game_converter.game_state_to_file(gs, '%s/%d.json' % (path, idx))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=u'主程序')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help=u'默认不输出。')
    parser.add_argument('-n', default=1,
                        type=int, help=u'游戏次数，默认只玩一次。')
    parser.add_argument('-o', '--path', default=None,
                        help=u'存档目录，默认不存档。')
    parser.add_argument('-s', '--seed', default=None,
                        type=int, help=u'设定随机种子，默认不设定')
    args = parser.parse_args()

    main(args.n, args.path, args.seed, args.verbose)
