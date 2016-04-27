# coding: utf-8
import os
import argparse
import json

import numpy as np

from AlphaLineupPuzzle import util
from AlphaLineupPuzzle import lineup_puzzle
from AlphaLineupPuzzle.preprocessing import state_to_tensor
from AlphaLineupPuzzle.preprocessing import action_to_tensor


class Save(object):

    @staticmethod
    def dump(gs, fn):
        fp = open(fn, 'w')
        save = {
            'size': gs.size,
            'score': gs.score,
            # alternative, ((idx, pos), next_alternative)+
            'history': gs.history,
        }
        json.dump(save, fp)
        fp.close()

    def load(self, fn):
        save = json.load(open(fn))
        self.size = save.get('size', 7)     # 兼容之前的版本
        self.score = save['score']
        history = save['history']
        self.__alternative, self._history = history[0], history[1:]

    # 以下三个接口是为了方便增广存档
    def set_transform(self, idx):
        self._alternative = list(self.__alternative)
        self.idx = idx

    @property
    def alternative(self):
        return [lineup_puzzle.Block.augment(b, self.idx) for b in self._alternative]

    @property
    def history(self):
        for (idx, pos), next_alternative in self._history:
            block_idx = self._alternative[idx]
            self._alternative[idx] = next_alternative
            shape = lineup_puzzle.Block._blocks[block_idx].shape
            action = idx, util.AUGMENT_POS[self.idx](pos, self.size, shape)
            yield action, lineup_puzzle.Block.augment(next_alternative, self.idx)


def _convert_game(save):
    '''
    转换指定存档文件中的每一步
    返回一个迭代器
    '''
    gs = lineup_puzzle.GameState.create(save.size, save.alternative)
    for action, next_alternative in save.history:
        state_tensor = state_to_tensor(gs)
        action_tensor = action_to_tensor(*action)
        yield state_tensor, action_tensor
        gs.move(*action, next_alternative=next_alternative)


def convert_game(save_filename):
    save = Save()
    save.load(save_filename)
    for idx in xrange(8):
        save.set_transform(idx)
        for state, action in _convert_game(save):
            yield state, action


def create_dataset_like(h5f, name, data, dtype):
    # 创建一个数据集
    dataset = h5f.create_dataset(name,
                                 dtype=dtype,
                                 shape=(1,) + data.shape,
                                 # None表示允许无限增长
                                 maxshape=(None,) + data.shape,
                                 chunks=(64,) + data.shape,
                                 compression='lzf')
    return dataset


def to_hdf5(sgf_files, hdf5_file):
    # http://docs.h5py.org/en/latest/high/group.html#Group.create_dataset
    import h5py as h5
    # make a hidden temporary file in case of a crash.
    # on success, this is renamed to hdf5_file
    dirname = os.path.dirname(hdf5_file)
    basename = os.path.basename(hdf5_file)
    tmp_file = os.path.join(dirname, '.tmp.' + basename)
    h5f = h5.File(tmp_file, 'w')

    count = 0
    for fn in sgf_files:
        for state, action in convert_game(fn):
            if count == 0:
                states = create_dataset_like(h5f, 'states', state, np.float32)
                actions = create_dataset_like(h5f, 'actions', action, np.int32)
            else:
                states.resize((count + 1,) + state.shape)
                actions.resize((count + 1,) + action.shape)
            states[count] = state
            actions[count] = action
            count += 1

    h5f.close()
    os.rename(tmp_file, hdf5_file)


def from_hdf5(hdf5_file):
    import h5py as h5
    h5f = h5.File(hdf5_file)
    return h5f['states'].value, h5f['actions'].value

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='#todo')
    parser.add_argument('infolder', help='游戏存档目录')
    parser.add_argument('-o', default='a.hdf5', help='输出目录')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    fns = os.listdir(args.infolder)
    fns = (os.path.join(args.infolder, fn) for fn in fns if fn.endswith('.json'))
    to_hdf5(fns, args.o)
