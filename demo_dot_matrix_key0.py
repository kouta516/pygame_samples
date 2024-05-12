""" dot matrix display demo in pygame (and minecraft)
dot_matrix_key0.py
        pygameのみ出力、自動のみ、クラスを使わず直接書いたもの
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
BACKGROUND_COLOR = pg_colors["darkolivegreen3"]
FPS = 30  # frames per second
wait = 0.03

# settings: matrix
m, n = 25, 12
dot_size, dot_intv = 15, 16
colors = {"on": "hotpink",
          "off": "antiquewhite1",
          "frame": "brown4"}
x0 = 5
y0 = 5

# settings: pygame key control
KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL = 800, 50  # for pygame.key.set_repeat(), in mSec

CTRL_X = {pygame.K_LEFT: -1, pygame.K_RIGHT: 1}
CTRL_Y = {pygame.K_UP: -1, pygame.K_DOWN: 1}


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

    clock = pygame.time.Clock()
    skip_frames1 = FPS * wait + 1

    x_change1, y_change1 = 0, 0

    update_flag = True
    running = True
    # infinite loop top ----
    while running:
        for event in pygame.event.get():
            # press ctrl-c or close the window to stop
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_ESCAPE:
                #     running = False
                if event.key in CTRL_X:
                    x_change1 = CTRL_X[event.key]
                    update_flag = True
                if event.key in CTRL_Y:
                    y_change1 = CTRL_Y[event.key]
                    update_flag = True
            if event.type == pygame.KEYUP:
                if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                    x_change1 = 0
                if event.key in {pygame.K_UP, pygame.K_DOWN}:
                    y_change1 = 0

        if update_flag and (skip_frames1 > FPS * wait):
            skip_frames1 = 0
            update_flag = False
            draw_dot(x1, y1, colors["off"])  # ドットを消す
            x1 += x_change1
            y1 += y_change1
            if x1 > m - 1:
                x1 = m - 1
            elif x1 < 0:
                x1 = 0
            if y1 > n - 1:
                y1 = n - 1
            elif y1 < 0:
                y1 = 0
            draw_dot(x1, y1, colors["on"])  # ドットを描く
            pygame.display.flip()  # update

        skip_frames1 += 1
        clock.tick(FPS)  # FPS, Frame Per Second
    # infinite loop bottom ----


# pygame setup
pygame.init()
pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)

screen = pygame.display.set_mode((SCREEN_SIZE["width"], SCREEN_SIZE["height"]))
pygame.display.set_caption(TITLE)
screen.fill(BACKGROUND_COLOR)
create_frame()

main()
pygame.quit()
