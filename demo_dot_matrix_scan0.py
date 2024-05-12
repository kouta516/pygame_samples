""" dot matrix display demo in pygame (and minecraft)
dot_matrix_scan0.py
        pygameのみ出力、Scannerクラスを追加して自動スキャンのみ、
"""
import os

import pygame
from pygame.colordict import THECOLORS as pg_colors
# see: https://www.pygame.org/docs/ref/color_list.html

file_name = os.path.basename(__file__)
dir_name = os.path.basename(os.path.dirname(__file__))
HELLO_MESSAGE = 'hello!! this is ' + file_name + ' in the ' + dir_name + ' !!'

# settings: pygame screen
TITLE = HELLO_MESSAGE
SCREEN_SIZE = {"width": 640, "height": 480}
BACKGROUND_COLOR = pg_colors["lavender"]
FPS = 15  # frames per second
wait = 0.1

# settings: matrix
m, n = 5, 7
dot_size, dot_intv = 15, 18
colors = {"on": "cyan2",
          "off": "darkgray",
          "frame": "lightgoldenrod1"}
x0 = 1
y0 = 1


class Scanner:
    """ スキャナーの動作を定義するクラス
    pos: 現在の点灯ドットの位置
    change: 点灯ドットの移動量
    direction: 点灯ドットの移動タイプ（"horizontal", "vertical"）
    auto_move(matrix): 点灯ドットを自動制御するメソッド
    """
    def __init__(self, pos=None, change=None, direction="horizontal"):
        self.pos = pos
        self.change = change
        self.direction = direction
        self.size = [m, n]

    def tick(self):
        if self.direction == "horizontal":
            self.auto_move(0, 1)
        if self.direction == "vertical":
            self.auto_move(1, 0)
        return self.pos

    def auto_move(self, i, j):
        self.pos[i] += self.change[i]
        self.pos[i] %= self.size[i]
        if ((self.change[i] > 0 and self.pos[i] == 0) or (self.change[i] < 0 and self.pos[i] == self.size[i] - 1)):
            self.pos[j] += self.change[j]
            self.pos[j] %= self.size[j]


def create_frame():
    # create the outer frame
    for y in range(-1, n + 1):
        for x in range(-1, m + 1):
            draw_dot(x, y, colors["frame"])
    # create the matrix
    for y in range(n):
        for x in range(m):
            draw_dot(x, y, colors["off"])


def draw_dot(x, y, color):
    color = pg_colors[color]
    left = (x0 + x) * dot_intv
    top = (y0 + y) * dot_intv
    width = dot_size
    height = dot_size
    pygame.draw.rect(screen, color,
                     pygame.Rect(left, top, width, height))


def main():
    x1, y1 = 2, 3
    draw_dot(x1, y1, colors["on"])
    x_change1, y_change1 = 1, -1

    scanner1 = Scanner(pos=[x1, y1], change=[x_change1, y_change1], direction="vertical")

    clock = pygame.time.Clock()
    skip_frames1 = FPS * wait + 1

    running = True
    # infinite loop top ----
    while running:
        for event in pygame.event.get():
            # press ctrl-c or close the window to stop
            if event.type == pygame.QUIT:
                running = False

        if skip_frames1 > FPS * wait:
            # print(f"(x1, y1): ({x1}, {y1})")
            skip_frames1 = 0
            draw_dot(x1, y1, colors["off"])  # ドットを消す
            x1, y1 = scanner1.tick()
            draw_dot(x1, y1, colors["on"])  # ドットを描く
            pygame.display.flip()  # update

        skip_frames1 += 1
        clock.tick(FPS)  # FPS, Frame Per Second
    # infinite loop bottom ----


# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE["width"], SCREEN_SIZE["height"]))
pygame.display.set_caption(TITLE)
screen.fill(BACKGROUND_COLOR)
create_frame()

main()
pygame.quit()
