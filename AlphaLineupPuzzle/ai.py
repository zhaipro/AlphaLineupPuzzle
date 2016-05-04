# coding: utf-8
import time
import argparse
import random

from AlphaLineupPuzzle import lineup_puzzle
from AlphaLineupPuzzle import models


def dbg(fmt, *args):
    print fmt % args


def quiet_dbg(fmt, *args):
    pass


def load_policy(name):
    if name == 'random':
        def policy(gs):
            actions = list(gs.legal_moves())
            return random.choice(actions), 1. / len(actions)
    else:
        policy_network = models.load_policy_network(name)

        def policy(gs):
            actions = policy_network(gs)
            return max(actions, key=lambda x: x[1])

    return policy


def load_ai(name):
    policy = load_policy(name)

    def ai(gs):
        gs = gs.copy()
        while any(gs.legal_moves()):
            action, p = policy(gs)
            gs.move(*action)
        return gs


def main(name, seconds, verbose):
    policy = load_policy(name)
    gs = lineup_puzzle.GameState.create()
    while any(gs.legal_moves()):
        dbg('score: %s', gs.score)
        dbg('%s', gs)
        action, p = policy(gs)
        dbg('%s %s', action, p)
        time.sleep(seconds)
        gs.move(*action)
    print gs.score
    print gs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='#todo')
    parser.add_argument('-i', help='模型名称')
    parser.add_argument('-s', '--seconds', default=0, type=float,
                        help='每次走子的时间间隔')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-c', '--count', default=1, type=int,
                        help='游戏次数')
    args = parser.parse_args()

    if not args.verbose:
        dbg = quiet_dbg     # NOQA
    for _ in xrange(args.count):
        main(args.i, args.seconds, args.verbose)
