# coding: utf-8
import numpy as np


AUGMENT_ARRAY = [
    lambda feature: feature,
    lambda feature: np.rot90(feature, 1),
    lambda feature: np.rot90(feature, 2),
    lambda feature: np.rot90(feature, 3),
    lambda feature: np.transpose(feature),
    lambda feature: np.flipud(feature),
    lambda feature: np.fliplr(np.rot90(feature, 1)),
    lambda feature: np.fliplr(feature),
]


def augment(array):
    # 旋转加镜面，共产生八个数据
    origin = np.array(array)
    for transform in AUGMENT_ARRAY:
        yield transform(origin)


AUGMENT_POS = [
    lambda pos, size, shape: pos,
    lambda pos, size, shape: (size - pos[1] - shape[1], pos[0]),
    lambda pos, size, shape: (size - pos[0] - shape[0], size - pos[1] - shape[1]),
    lambda pos, size, shape: (pos[1], size - pos[0] - shape[0]),
    lambda pos, size, shape: (pos[1], pos[0]),
    lambda pos, size, shape: (size - pos[0] - shape[0], pos[1]),
    lambda pos, size, shape: (size - pos[1] - shape[1], size - pos[0] - shape[0]),
    lambda pos, size, shape: (pos[0], size - pos[1] - shape[1]),
]


def augment_pos(pos, size, shape):
    for transform in AUGMENT_POS:
        yield transform(pos, size, shape)
