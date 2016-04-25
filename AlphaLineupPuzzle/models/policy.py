# coding: utf-8
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L


class Policy(chainer.Chain):

    def __init__(self, in_dim, out_dim):
        super(Policy, self).__init__(
            l1=L.Linear(in_dim, out_dim),
        )

    def dump(self):
        pass

    def load(self):
        pass

    def forward(self, x):
        if not isinstance(x, chainer.Variable):
            if not isinstance(x, np.ndarray) or x.dtype != np.float32:
                x = np.array(x, dtype=np.float32)
            x = chainer.Variable(x)
        return self.l1(x)

    def __call__(self, x):
        return self.forward(x)
