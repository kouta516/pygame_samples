""" dot matrix display demo in pygame (and minecraft)
dot_matrix_pg1.py
        pygameのみ出力、自動移動のみ（水平移動のみ）
        Matrixクラスを使ってクラス化、インスタンスは2つ
"""
import os

import pygame
from pygame.colordict import THECOLORS as pg_colors
# see: https://www.pygame.org/docs/ref/color_list.html


class Matrix:
    def __init__(self, screen, m=5, n=7, dot_size=15, dot_intv=18, colors=None, wait=0.1, x0=1, y0=1):
        self.screen = screen
        self.m = m
        self.n = n
        self.dot_size = dot_size
        self.dot_intv = dot_intv
        self.colors = colors
        self.wait = wait
        self.x0 = x0
        self.y0 = y0

        self.create_frame()

    def create_frame(self):
        # create the outer frame
        for y in range(-1, self.n + 1):
            for x in range(-1, self.m + 1):
                self.draw_dot(x, y, self.colors["frame"])
        # create the matrix
        for y in range(self.n):
            for x in range(self.m):
                self.draw_dot(x, y, self.colors["off"])

    def draw_dot(self, x, y, color):
        color = pg_colors[color]
        left = (self.x0 + x) * self.dot_intv
        top = (self.y0 + y) * self.dot_intv
        width = self.dot_size
        height = self.dot_size
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(left, top, width, height))


if __name__ == "__main__":
    file_name = os.path.basename(__file__)
    dir_name = os.path.basename(os.path.dirname(__file__))
    HELLO_MESSAGE = 'hello!! this is ' + file_name + ' in the ' + dir_name + ' !!'

    # settings: pygame screen
    TITLE = HELLO_MESSAGE
    SCREEN_SIZE = {"width": 640, "height": 480}
    BACKGROUND_COLOR = pg_colors["lavender"]
    FPS = 15  # frames per second

    def init_setup():
        # pygame setup
        pygame.init()

        screen = pygame.display.set_mode((SCREEN_SIZE["width"], SCREEN_SIZE["height"]))
        pygame.display.set_caption(TITLE)
        screen.fill(BACKGROUND_COLOR)

        # matrix instances
        matrix1 = Matrix(screen=screen,
                         m=5, n=7,
                         dot_size=15, dot_intv=18,
                         colors={"on": "cyan2",
                                 "off": "darkgray",
                                 "frame": "lightgoldenrod1"},
                         wait=0.5,
                         x0=1, y0=1)

        matrix2 = Matrix(screen=screen,
                         m=24, n=8,
                         dot_size=13, dot_intv=14,
                         colors={"on": "magenta3",
                                 "off": "limegreen",
                                 "frame": "lightyellow3"},
                         wait=0.05,
                         x0=15, y0=15)

        return matrix1, matrix2

    def main(setup):
        matrix1, matrix2 = setup
        # matrix1 setup
        x1, y1 = 2, 3
        x_change1, y_change1 = 1, -1
        # matrix2 setup
        x2, y2 = 1, 1
        x_change2, y_change2 = -1, 1

        clock = pygame.time.Clock()
        skip_frames1 = FPS * matrix1.wait + 1
        skip_frames2 = FPS * matrix2.wait + 1

        running = True
        # infinite loop top ----
        while running:
            for event in pygame.event.get():
                # press ctrl-c or close the window to stop
                if event.type == pygame.QUIT:
                    running = False

            if skip_frames1 > FPS * matrix1.wait:
                # print(f"(x1, y1): ({x1}, {y1})")
                skip_frames1 = 0
                matrix1.draw_dot(x1, y1, matrix1.colors["off"])  # ドットを消す
                x1 += x_change1
                x1 %= matrix1.m
                if ((x_change1 > 0 and x1 == 0) or (x_change1 < 0 and x1 == matrix1.m - 1)):
                    y1 += y_change1
                    y1 %= matrix1.n
                matrix1.draw_dot(x1, y1, matrix1.colors["on"])  # ドットを描く
                pygame.display.flip()  # update

            if skip_frames2 > FPS * matrix2.wait:
                skip_frames2 = 0
                matrix2.draw_dot(x2, y2, matrix2.colors["off"])  # ドットを消す
                x2 += x_change2
                x2 %= matrix2.m
                if ((x_change2 > 0 and x2 == 0) or (x_change2 < 0 and x2 == matrix2.m - 1)):
                    y2 += y_change2
                    y2 %= matrix2.n
                matrix2.draw_dot(x2, y2, matrix2.colors["on"])  # ドットを描く
                pygame.display.flip()  # update

            skip_frames1 += 1
            skip_frames2 += 1
            clock.tick(FPS)  # FPS, Frame Per Second
        # infinite loop bottom ----

    main(init_setup())
    pygame.quit()
