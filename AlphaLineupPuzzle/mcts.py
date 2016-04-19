# coding: utf-8
import random
import math


class StateNode(object):

    # 这将会是一颗巨大的搜索树
    # 以下语句可以节省大量内存
    __slots__ = ('gs', 'value', 'children', 'depth')

    def __init__(self, gs, depth):
        self.gs = gs
        self.value = 0
        self.children = None
        self.depth = depth

    def select(self):
        for child in self.children:
            if child.n < 2:
                return child

        max_child = None
        max_value = 0
        for child in self.children:
            dalta = (child.value - child.gs.score)

            a = child.value + dalta / math.sqrt(child.n)
            if a > max_value:
                max_value = a
                max_child = child
        return max_child

    def simulate(self):
        return self.gs.score

    def visit(self):
        if self.depth == 0:
            value = self.simulate()
        else:
            if self.children is None:
                self.ext()
            child = self.select()
            if child:
                child.visit()
                value = child.value
            else:   # Game Over
                value = self.gs.score
        value = float(value)
        self.update(value)

    def is_leaf(self):
        return self.depth == 0

    def update(self, value):
        if self.children:
            child = max(self.children)
            self.value = child.value
        else:
            self.value = value

    def ext(self):
        self.children = []
        for action in self.gs.legal_moves():
            gs = self.gs.copy()
            an = ActionNode(gs, action, self.depth)
            self.children.append(an)

    @staticmethod
    def get_move(gs, depth, times):
        root = StateNode(gs, depth)

        for _ in xrange(times):
            root.visit()

        if root.children:
            child = max(root.children)
            return child.action, child.value
        else:
            return None, 0


class ActionNode(StateNode):

    __slots__ = ('n', 'action')

    def __init__(self, gs, action, depth):
        super(ActionNode, self).__init__(gs, depth)
        self.n = 0
        self.action = action
        self.gs = gs.copy()
        self.gs.move(*action)

    def __lt__(self, other):
        return self.value < other.value

    def update(self, value):
        self.value = (self.n * self.value + value) / (self.n + 1)
        self.n += 1

    def select(self):
        return random.choice(self.children)

    def ext(self):
        self.children = []
        for gs in self.gs.ext(self.action[0]):
            gs = gs.copy()
            sn = StateNode(gs, self.depth - 1)
            self.children.append(sn)


def get_move(gs):
    return StateNode.get_move(gs, 4, 6000)
