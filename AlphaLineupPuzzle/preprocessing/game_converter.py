# coding: utf-8
import os
import argparse
import json

from AlphaLineupPuzzle import lineup_puzzle
from AlphaLineupPuzzle.preprocessing import state_to_tensor
from AlphaLineupPuzzle.preprocessing import action_to_tensor


def game_state_to_file(gs, fn):
    assert gs.history
    fp = open(fn, 'w')
    json.dump({'history': gs.history, 'score': gs.score}, fp)
    fp.close()


def convert_game(in_fn):
    '''
    转换指定存档文件中的每一步
    返回一个迭代器
    '''
    save = json.load(open(in_fn))
    score, history = save['score'], save['history']
    lineup_puzzle.Block.init()
    gs = lineup_puzzle.GameState.create(alternative=history[0])
    for action, next_alternative in history[1:]:
        state_tensor = state_to_tensor(gs)
        action_tensor = action_to_tensor(*action)
        yield state_tensor, action_tensor
        gs.move(*action, next_alternative=next_alternative)


def to_hdf5(sgf_files, hdf5_file):
    import h5py as h5
    # make a hidden temporary file in case of a crash.
    # on success, this is renamed to hdf5_file
    dirname = os.path.dirname(hdf5_file)
    basename = os.path.basename(hdf5_file)
    tmp_file = os.path.join(dirname, '.tmp.' + basename)
    h5f = h5.File(tmp_file, 'w')

    count = 0
    for fn in sgf_files:`
        for state, action in convert_game(fn):
            h5f.create_dataset('state_%d' % count, data=state, compression='lzf')
            h5f.create_dataset('action_%d' % count, data=action, compression='lzf')
            count += 1

    h5f.close()

    os.rename(tmp_file, hdf5_file)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='#todo')
    parser.add_argument('infolder', help='游戏存档目录')
    parser.add_argument('-o', default='a.hdf5', help='输出目录')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    fns = os.listdir(args.infolder)
    fns = (os.path.join(args.infolder, fn) for fn in fns)
    to_hdf5(fns, args.o)
