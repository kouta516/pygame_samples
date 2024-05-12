""" dot matrix display class for pygame and minecraft
class Matrix:  # parent class
class MatrixPG(Matrix):  # child class for pygame
    def __init__(self, screen, m=5, n=7, dot_size=15, dot_intv=18, colors=None, x0=1, y0=1):
class MatrixMC(Matrix):  # child class for minecraft
    def __init__(self, mc, m=5, n=7, colors=None, x0=1, y0=1, z0=1)
class Scanner:  # scanner class
    def __init__(self, matrix, pos=None, change=None, wait=0.2, direction="horizontal"):

The sample part after 'if __name__ == "__main__":' is code for minecraft and not including one for minecraft.
"""
import os

# for pygame
import pygame
from pygame.colordict import THECOLORS as pg_colors
# see: https://www.pygame.org/docs/ref/color_list.html

# for minecraft
from mcje.minecraft import Minecraft
import param_MCJE as param


class Matrix:  # parent class
    """
    m、n: matrixの列数、行数
    colors: ドットの色の辞書
    with_frame: フレームの有無
    create_frame(): フレームの作成
    fill_matrix(): マトリックスの作成
    draw_frame(): フレームの描画
    draw_dot(): ドットの描画  # 子クラスでオーバーライドする
    """
    def __init__(self, m, n, colors, with_frame):
        self.m = m
        self.n = n
        self.colors = colors
        self.with_frame = with_frame
        self.create_frame()

    def create_frame(self):
        if self.with_frame:
            self.draw_frame(self.colors["frame"])
        else:
            self.draw_frame(color=self.colors["background"])
        self.fill_matrix(color=self.colors["off"])

    def draw_frame(self, color):
        # create the outer frame
        for y in range(-1, self.n + 1):
            for x in range(-1, self.m + 1):
                self.draw_dot((x, y), color)

    def fill_matrix(self, color):
        # create the matrix
        for y in range(self.n):
            for x in range(self.m):
                self.draw_dot((x, y), color)

    def draw_dot(self, pos, color):
        pass


class Scanner:
    """ スキャナーの動作を定義するクラス
    matrix: スキャナーが動作するMatrixクラスのインスタンス
    pos: 現在の点灯ドットの位置
    change: 点灯ドットの移動量
    wait: 点灯ドットの移動間隔（秒）
    direction: 点灯ドットの移動タイプ（"horizontal", "vertical", or "control"）
    control_move(matrix): 点灯ドットをキー入力でコントロールするメソッド
    auto_move(matrix): 点灯ドットを自動制御するメソッド
    """
    def __init__(self, matrix, pos=None, change=None, wait=0.2, direction="horizontal"):
        self.matrix = matrix
        self.pos = pos
        self.change = change
        self.wait = wait
        self.direction = direction
        self.size = [self.matrix.m, self.matrix.n]
        self.matrix.draw_dot(self.pos, self.matrix.colors["on"])

    def set_change(self, change):
        self.change = change
        if self.matrix.output == "minecraft":
            self.change = (self.change[0], 0 - self.change[1])

    def tick(self):
        self.matrix.draw_dot(self.pos, self.matrix.colors["off"])  # 現在の点灯ドットを消す
        if self.direction == "horizontal":
            self.auto_move(0, 1)
        if self.direction == "vertical":
            self.auto_move(1, 0)
        if self.direction == "control":
            self.control_move()
        self.matrix.draw_dot(self.pos, self.matrix.colors["on"])  # 次のドットを描く

    def auto_move(self, i, j):
        self.pos[i] += self.change[i]
        self.pos[i] %= self.size[i]
        if ((self.change[i] > 0 and self.pos[i] == 0) or (self.change[i] < 0 and self.pos[i] == self.size[i] - 1)):
            self.pos[j] += self.change[j]
            self.pos[j] %= self.size[j]

    def control_move(self):
        self.pos[0] += self.change[0]
        self.pos[1] += self.change[1]
        if self.pos[0] > self.matrix.m - 1:
            self.pos[0] = self.matrix.m - 1
        elif self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] > self.matrix.n - 1:
            self.pos[1] = self.matrix.n - 1
        elif self.pos[1] < 0:
            self.pos[1] = 0


class MatrixPG(Matrix):
    """
    pygameでのMatrixクラスの子クラス
    screen: pygameのスクリーン
    m、n: matrixの列数、行数
    dot_size: ドットのサイズ
    dot_intv: ドット間の間隔
    colors: ドットの色の辞書
    with_frame: フレームの有無
    x0: matrixの左上のx座標
    y0: matrixの左上のy座標
     """
    def __init__(self, screen, m=5, n=7, dot_size=15, dot_intv=18, colors=None, with_frame=True, x0=1, y0=1):
        # colors=Noneとしておき、あとでクラス変数としてデフォルト値を設定する。
        # colors=[]など、引数に辞書やリストなどのミュータブルなオブジェクトを指定するのは避けるべし。
        self.output = "pygame"
        self.screen = screen
        self.dot_size = dot_size
        self.dot_intv = dot_intv
        if colors is None:
            colors = {"on": "cyan2",
                      "off": "darkgray",
                      "frame": "lightgoldenrod1",
                      "background": "lavender"}
        self.x0 = x0
        self.y0 = y0
        super().__init__(m, n, colors=colors, with_frame=with_frame)

    def draw_dot(self, pos, color):
        x, y = pos
        color = pg_colors[color]
        left = (self.x0 + x) * self.dot_intv
        top = (self.y0 + y) * self.dot_intv
        width = self.dot_size
        height = self.dot_size
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(left, top, width, height))


class MatrixMC(Matrix):
    """
    minecraftでのMatrixクラスの子クラス
    mc: minecraftのクライアント
    m、n: matrixの列数、行数
    colors: ドットの色の辞書
    with_frame: フレームの有無
    x0: matrixの左上のx座標
    y0: matrixの左上のy座標
    z0: matrixの左上のz座標
    """
    def __init__(self, mc, m=5, n=7, colors=None, with_frame=True, x0=1, y0=1, z0=1):
        self.output = "minecraft"
        self.mc = mc
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        if colors is None:
            self.colors = {"on": "GOLD_BLOCK",
                           "off": "IRON_BLOCK",
                           "frame": "SEA_LANTERN_BLOCK",
                           "background": "AIR"}
        super().__init__(m, n, colors=colors, with_frame=with_frame)

    def draw_dot(self, pos, color):
        x, y = pos
        color = getattr(param, color)
        self.mc.setBlock(self.x0 + x, self.y0 + y, self.z0, color)


if __name__ == "__main__":
    file_name = os.path.basename(__file__)
    dir_name = os.path.basename(os.path.dirname(__file__))
    HELLO_MESSAGE = 'hello!! this is ' + file_name + ' in the ' + dir_name + ' !!'
    
    # settings: pygame screen
    TITLE = HELLO_MESSAGE
    SCREEN_SIZE = {"width": 640, "height": 480}
    BACKGROUND_COLOR = pg_colors["lavender"]
    FPS = 60  # frames per second

    def init_setup():
        # pygame setup
        pygame.init()

        screen = pygame.display.set_mode((SCREEN_SIZE["width"], SCREEN_SIZE["height"]))
        pygame.display.set_caption(TITLE)
        screen.fill(BACKGROUND_COLOR)
        pygame.display.flip()

        # minecraft setup
        mc = Minecraft.create(port=param.PORT_MC)
        mc.postToChat(HELLO_MESSAGE)

        # clear the field in Minecraft
        # mc.setBlocks(-50, param.Y_SEA + 5, 18,
        #              50, param.Y_SEA + 50, 20, param.AIR)

        # matrix instances
        matrix1 = MatrixPG(screen=screen, m=5, n=7, dot_size=15, dot_intv=18,
                           colors={"on": "cyan2",
                                   "off": "darkgray",
                                   "frame": "lightgoldenrod1",
                                   "background": "lavender"},
                           with_frame=False,
                           x0=1, y0=1)
        matrix2 = MatrixPG(screen=screen, m=16, n=10, dot_size=12, dot_intv=18,
                           colors={"on": "red",
                                   "off": "palegreen3",
                                   "frame": "maroon3",
                                   "background": "lavender"},
                           with_frame=True,
                           x0=8, y0=8)

        matrices = [matrix1, matrix2]
        scanners = [Scanner(matrices[0], pos=[0, 0], change=[-1, -1], wait=0.2, direction="vertical"),
                    Scanner(matrices[1], pos=[0, 0], change=[1, 1], wait=0.1, direction="horizontal")]

        return matrices, scanners

    def update_matrices(matrices, scanners, skip_frames):
        for i, matrix in enumerate(matrices):
            if skip_frames[i] > FPS * scanners[i].wait:
                skip_frames[i] = 0
                scanners[i].tick()
            skip_frames[i] += 1
            if matrix.output == "pygame":
                pygame.display.flip()

    def main(setup):
        matrices, scanners = setup

        skip_frames = [0, 0, 0, 0]
        clock = pygame.time.Clock()
        running = True
        # infinite loop top ----
        while running:
            for event in pygame.event.get():
                # press ctrl-c or close the window to stop
                if event.type == pygame.QUIT:
                    running = False

            # update_matrices
            update_matrices(matrices, scanners, skip_frames)

            clock.tick(FPS)  # FPS, Frame Per Second
        # infinite loop bottom ----

    main(init_setup())
    pygame.quit()
