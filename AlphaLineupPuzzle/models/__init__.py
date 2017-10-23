# coding: utf-8
import numpy as np
import chainer.links as L
import chainer.functions as F
from chainer import serializers, Variable

import policy
from AlphaLineupPuzzle.preprocessing import preprocessing


def load_policy_network(name):
    in_dim = preprocessing.state_to_tensor.features
    out_dim = preprocessing.action_to_tensor.features
    model = L.Classifier(policy.Policy(in_dim, out_dim))
    serializers.load_npz('%s.model.npz' % name, model)

    def policy_network(gs):
        state = preprocessing.state_to_tensor(gs)
        Y = model.predictor([state]).data[0]

        actions = []
        for idx, pos in gs.legal_moves():
            action = preprocessing.action_to_tensor(gs, idx, pos, gs.size)
            actions.append(action)

        # 确保即使actions为空列表，也要构造一个int型的空np数组
        actions = np.array(actions, dtype=np.int32)
        Y = Y[actions]
        Y = Y.reshape((1, Y.size))
        Y = Variable(Y)

        P = F.softmax(Y).data[0]

        for idx, pos in enumerate(gs.legal_moves()):
            yield pos, P[idx]

    return policy_network
