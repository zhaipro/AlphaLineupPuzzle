# coding: utf-8
from __future__ import unicode_literals
import argparse

import numpy as np

from lineup_puzzle import GameState
import mcts
from preprocessing import game_converter


def play(verbose):
    blocks = raw_input('>>> ')
    blocks = map(int, blocks.split())
    gs = GameState.create(alternative=blocks)
    if verbose:
        print gs
    while True:
        action, value = mcts.get_move(gs)
        if action is None:
            break
        gs.move(*action)
        if verbose:
            print action, value, gs.score, value - gs.score
            print gs
        if args.interaction:
            block = raw_input('>>> ')
            block = int(block)
            gs.alternative[action[0]] = block
    return gs


def main(n, path, seed, verbose):
    if seed:
        np.random.seed(seed)

    if args.interaction:
        for idx, block in enumerate(Block.blocks):
            print '--- %d ---' % idx
            print Block.to_str(block)

    for idx in xrange(n):
        gs = play(verbose)
        if path:
            game_converter.game_state_to_file(gs, '%s/%d.json' % (path, idx))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='主程序')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='默认不输出。')
    parser.add_argument('-n', default=1,
                        type=int, help='游戏次数，默认只玩一次。')
    parser.add_argument('-o', '--path', default=None,
                        help='存档目录，默认不存档。')
    parser.add_argument('-s', '--seed', default=None,
                        type=int, help='设定随机种子，默认不设定')
    parser.add_argument('-i', '--interaction', default=False,
                        action='store_true', help=u'交互式')
    args = parser.parse_args()

    main(args.n, args.path, args.seed, args.verbose)
