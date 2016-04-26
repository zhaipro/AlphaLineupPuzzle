# coding: utf-8
import argparse

import numpy as np
import chainer
from chainer import Variable, optimizers, serializers
import chainer.links as L

from AlphaLineupPuzzle.models import policy
from AlphaLineupPuzzle.preprocessing import game_converter


def test(model, X, Y, batchsize=100, verbose=False):     # NOQA
    # evaluation
    sum_accuracy = 0
    sum_loss = 0
    for i in xrange(0, len(X), batchsize):
        x = chainer.Variable(X[i:i + batchsize], volatile='on')
        t = chainer.Variable(Y[i:i + batchsize], volatile='on')
        loss = model(x, t)
        sum_loss += float(loss.data) * len(t.data)
        sum_accuracy += float(model.accuracy.data) * len(t.data)

    if verbose:
        print('test mean loss=%s, accuracy=%s' % (
            sum_loss / len(X), sum_accuracy / len(X)))


def training(X, Y, n=20, alpha=0.01, batchsize=100, verbose=False):     # NOQA
    simples = len(X)
    X_train, X_test = np.split(X, [int(simples * 0.9 + 0.5)])
    Y_train, Y_test = np.split(Y, [int(simples * 0.9 + 0.5)])

    # 抱歉这里硬编码了
    model = L.Classifier(policy.Policy(X_train[0].size, 7 * 7 * 3))
    optimizer = optimizers.SGD(alpha)
    optimizer.setup(model)
    datasize = len(X_train)
    for epoch in xrange(n):
        if verbose:
            print 'epoch %d' % epoch
        indexes = np.random.permutation(datasize)
        sum_accuracy = 0
        sum_loss = 0
        for i in range(0, datasize, batchsize):
            x = Variable(X_train[indexes[i: i + batchsize]])
            t = Variable(Y_train[indexes[i: i + batchsize]])
            optimizer.update(model, x, t)

            sum_loss += float(model.loss.data) * len(t.data)
            sum_accuracy += float(model.accuracy.data) * len(t.data)
        print 'train mean loss=%s, accuracy=%s' % (
            sum_loss / len(X_train), sum_accuracy / len(X_train))

    # Save the model and the optimizer
    if verbose:
        print('save the model')
    serializers.save_npz('mlp.model', model)
    if verbose:
        print('save the optimizer')
    serializers.save_npz('mlp.state', optimizer)

    test(model, X_test, Y_test, verbose=verbose)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='#todo')
    parser.add_argument('-i', help='由game_converter.py转换来的训练数据的文件名')
    parser.add_argument('-a', '--alpha', type=float, help='学习速率')
    parser.add_argument('-b', '--batch', type=int, help='批次')
    parser.add_argument('-n', type=int, help='迭代次数')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    states, actions = game_converter.from_hdf5(args.i)
    training(states, actions, args.n, args.alpha, args.batch, args.verbose)
