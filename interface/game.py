# coding: utf-8
'''
功能：
  读取游戏存档，查看游戏过程
  实时演示AI下法
  人机交互，连续输入真实游戏的状态，输出AI选择的下法
棋盘数据：
  pc: 394 700
  iPhone分辨率：750 1334
  每个格子间隔：13像素
  每个格子的宽度：85像素
  棋盘坐标：37, 1054
'''
import pyglet
import cocos
from cocos import actions
from cocos.director import director

background = 'res/background.png'
block = 'res/block.png'

CAPTION = 'AlphaLineupPuzzle'
WIDTH, HEIGHT = 394, 700
IPHONE_WIDTH, IPHONE_HEIGHT = 750, 1334
PINK = (255, 137, 137, 255)


class Block(cocos.sprite.Sprite):
    '粉红小方块'

    _img = None
    _hide = None
    _show = None

    def __init__(self):
        if Block._img is None:
            Block._img = pyglet.image.load(block)
            Block._hide = actions.Hide()
            Block._show = actions.Show()
        super(Block, self).__init__(Block._img)

    def show(self):
        self.do(Block._show)

    def hide(self):
        self.do(Block._hide)


class Label(cocos.text.Label):

    def __init__(self, text, **kw):
        super(Label, self).__init__(text,
                                    font_name='Times New Roman',
                                    font_size=44,
                                    color=PINK,
                                    **kw)


class Board(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(Board, self).__init__()
        bg = cocos.sprite.Sprite(background)
        # 精灵的默认锚点在中心位置
        bg.image_anchor = 0, 0
        self.add(bg)

        self.score_bar = Label('1234567890', anchor_x='right')
        self.score_bar.position = (720, 1270)
        self.add(self.score_bar)

        # 用于输出调试信息
        self.info_bar = Label('ready')
        self.info_bar.position = (10, 10)   # 留白
        self.add(self.info_bar)

        self.blocks = []
        for y in xrange(7):
            self.blocks.append([])
            for x in xrange(7):
                b = Block()
                b.position = 37 + 85 * x, 1054 - 85 * y
                self.blocks[y].append(b)

    def next_game_state(self):
        raise NotImplementedError()

    def prev_game_state(self):
        raise NotImplementedError()

    def update_baord(self, board):
        for y in xrange(7):
            for x in xrange(7):
                if board[y][x]:
                    self.blocks[y][x].show()
                else:
                    self.blocks[y][x].hide()

    def update_score(self, score):
        self.score_bar.element.text = str(score)

    def update(self, gs):
        # 只支持7x7的棋盘
        assert gs.size == 7
        self.update_baord(gs.board)
        self.update_score(gs.score)

    def update_text(self, key):
        '输出调试信息'
        s = 'key: %r' % key
        self.info_bar.element.text = s

    def on_key_release(self, key, modifiers):
        KEY_UP = 65362
        KEY_DOWN = 65364
        KEY_LEFT = 65361
        KEY_RIGHT = 65363

        if key == KEY_RIGHT:
            pass

        self.update_text(key)


def start():
    director.init(width=WIDTH, height=HEIGHT, caption=CAPTION)
    board_layer = Board()
    main_scene = cocos.scene.Scene(board_layer)
    # 场景按照iPhone6s的尺寸进行开发
    # 最后缩放到窗口尺寸
    main_scene.anchor = 0, 0
    main_scene.scale = float(WIDTH) / IPHONE_WIDTH
    director.run(main_scene)

if __name__ == '__main__':
    start()
