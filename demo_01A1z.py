""" dotmatrix demo in pygame (and minecraft)
"""
import pygame
from pygame.locals import Rect
from pygame.colordict import THECOLORS as pg_colors
# see: https://www.pygame.org/docs/ref/color_list.html

# settings: screen and UI
TITLE = "hello!! moving dot on the matrix!!"
WIDTH, HEIGHT = 640, 480
BACKGROUND_COLOR = pg_colors["lavender"]
FPS = 15  # frames per second
WAIT1 = 0.25


class Matrix:
    def __init__(self, screen, m=5, n=7, dot_size=15, dot_intv=18, x0=1, y0=1):
        self.screen = screen
        self.m = m
        self.n = n
        self.dot_size = dot_size
        self.dot_intv = dot_intv
        self.x0 = x0
        self.y0 = y0
        # self.set_colors()

    def create_frame(self):
        # create the outer frame
        for y in range(-1, self.n + 1):
            for x in range(-1, self.m + 1):
                self.draw_frame(x, y)
        # create the matrix
        for y in range(self.n):
            for x in range(self.m):
                self.erase_dot(x, y)

    def set_colors(self, on="burlywood4", off="darkgray", frame="lightsteelblue2"):
        self.colors = {"on": pg_colors[on],
                       "off": pg_colors[off],
                       "frame": pg_colors[frame]}

    def change_color_on(self, color):
        self.colors["on"] = pg_colors[color]

    def draw_dot(self, x, y):
        pygame.draw.rect(self.screen, self.colors["on"],
                         Rect((self.x0 + x) * self.dot_intv, (self.y0 + y) * self.dot_intv, self.dot_size, self.dot_size))

    def erase_dot(self, x, y):
        pygame.draw.rect(self.screen, self.colors["off"],
                         Rect((self.x0 + x) * self.dot_intv, (self.y0 + y) * self.dot_intv, self.dot_size, self.dot_size))

    def draw_frame(self, x, y):
        pygame.draw.rect(self.screen, self.colors["frame"],
                         Rect((self.x0 + x) * self.dot_intv, (self.y0 + y) * self.dot_intv, self.dot_size, self.dot_size))

    def move_dot(self, x, y, x_change, y_change):
        x += x_change
        y += y_change
        if x > self.m - 1:
            x = self.m - 1
        elif x < 0:
            x = 0
        if y > self.n - 1:
            y = self.n - 1
        elif y < 0:
            y = 0
        return x, y


def pg_setup():
    pygame.init()

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption(TITLE)
    screen.fill(BACKGROUND_COLOR)

    matrix1 = Matrix(screen=screen, m=5, n=7, dot_size=15, dot_intv=18, x0=1, y0=1)
    matrix1.set_colors(on="cyan2", off="darkgray", frame="lightgoldenrod1")
    matrix1.create_frame()

    return matrix1


def main(setup):
    matrix1 = setup
    x1, y1 = 2, 3
    matrix1.draw_dot(x1, y1)
    x_change1, y_change1 = 1, 0

    clock = pygame.time.Clock()
    skip_frames1 = FPS * WAIT1 + 1

    running = True
    # infinite loop top ----
    while running:
        for event in pygame.event.get():
            # press ctrl-c or close the window to stop
            if event.type == pygame.QUIT:
                running = False

        if skip_frames1 > FPS * WAIT1:
            # print(f"(x1: {x1}, y1: {y1})")
            skip_frames1 = 0
            matrix1.erase_dot(x1, y1)  # ドットを消す
            x1 += x_change1
            x1 %= matrix1.m
            if x1 == 0:
                y1 += y_change1
                y1 %= matrix1.n
            matrix1.draw_dot(x1, y1)  # ドットを描く
            pygame.display.flip()  # update

        skip_frames1 += 1
        clock.tick(FPS)  # FPS, Frame Per Second
    # infinite loop bottom ----


main(pg_setup())
pygame.quit()
