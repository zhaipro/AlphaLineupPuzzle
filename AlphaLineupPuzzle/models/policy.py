# coding: utf-8
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L


class Add(chainer.Function):
    def forward_cpu(self, inputs):
        # do forward computation on CPU
        a, b = inputs
        return np.transpose(np.transpose(a, (2, 3, 0, 1)) + b, (2, 3, 0, 1)),

    def backward_cpu(self, inputs, gy):
        # do backward computation on CPU
        gy = gy[0]
        return gy, gy.sum(axis=(2, 3))


class Reshape(chainer.Function):

    def __init__(self, shape):
        super(Reshape, self).__init__()
        if isinstance(shape, tuple):
            self.shape = shape
        else:
            self.shape = (shape,)

    def forward_cpu(self, inputs):
        a = inputs[0]
        return a.reshape((a.shape[0],) + self.shape),

    def backward_cpu(self, inputs, gy):
        a = inputs[0]
        return gy[0].reshape(a.shape),


def reshape(x, shape):
    return Reshape(shape)(x)


class Policy(chainer.Chain):

    def __init__(self, in_dim, out_dim, ks=50):
        super(Policy, self).__init__(
            c1=L.Convolution2D(4, ks, 5, pad=2),
            l1=L.Linear(19 * 3, ks, nobias=True),
            c2=L.Convolution2D(ks, ks, 3, pad=1),
            cl=L.Convolution2D(ks, 3, 1),
        )

    def forward(self, x, b):
        if not isinstance(x, chainer.Variable):
            if not isinstance(x, np.ndarray) or x.dtype != np.float32:
                x = np.array(x, dtype=np.float32)
                b = np.array(b, dtype=np.float32)
            x = chainer.Variable(x)
            b = chainer.Variable(b)
        h1 = F.relu(Add()(self.c1(x), self.l1(b)))
        h2 = F.relu(self.c2(h1))
        return reshape(self.cl(h2), 3 * 7 * 7)

    def __call__(self, x):
        volatile = x.volatile
        x = x.data
        x, b = x[:, 3 * 19:], x[:, :3 * 19]
        x = x.reshape((x.shape[0], 4, 7, 7))
        x = chainer.Variable(x, volatile)
        b = chainer.Variable(b, volatile)
        return self.forward(x, b)
