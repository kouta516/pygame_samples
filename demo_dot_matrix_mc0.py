""" dot matrix display demo in pygame (and minecraft)
dot_matrix_mc0.py
        一つのMatrixをpygame/マイクラ同時出力、自動のみ、クラスなし
"""
import os

# for pygame
import pygame
from pygame.colordict import THECOLORS as pg_colors
# see: https://www.pygame.org/docs/ref/color_list.html

# for minecraft
from mcje.minecraft import Minecraft
import param_MCJE as param


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
colors_mc = {"on": "GOLD_BLOCK",
             "off": "IRON_BLOCK",
             "frame": "SEA_LANTERN_BLOCK"}

# settings: matrix position for pygame/minecraft
x0 = 1
y0 = 1

x0_mc = 0
y0_mc = param.Y_SEA + 20
Z0_mc = 5


def create_frame():
    # create the outer frame
    for y in range(-1, n + 1):
        for x in range(-1, m + 1):
            draw_dot(x, y, colors["frame"])
            draw_dot_mc(x, y, colors_mc["frame"])
    # create the matrix
    for y in range(n):
        for x in range(m):
            draw_dot(x, y, colors["off"])
            draw_dot_mc(x, y, colors_mc["off"])


def draw_dot(x, y, color):
    color = pg_colors[color]
    left = (x0 + x) * dot_intv
    top = (y0 + y) * dot_intv
    width = dot_size
    height = dot_size
    pygame.draw.rect(screen, color,
                     pygame.Rect(left, top, width, height))


def draw_dot_mc(x, y, color):
    block_id = getattr(param, color)
    mc.setBlock(x0_mc + x, y0_mc + y, Z0_mc, block_id)


def main():
    x1, y1 = 2, 3
    draw_dot(x1, y1, colors["on"])
    x_change1, y_change1 = 1, -1

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
            draw_dot_mc(x1, y1, colors_mc["off"])  # ドットを消す
            x1 += x_change1
            x1 %= m
            if ((x_change1 > 0 and x1 == 0) or (x_change1 < 0 and x1 == m - 1)):
                y1 += y_change1
                y1 %= n
            draw_dot(x1, y1, colors["on"])  # ドットを描く
            draw_dot_mc(x1, y1, colors_mc["on"])  # ドットを描く
            pygame.display.flip()  # update

        skip_frames1 += 1
        clock.tick(FPS)  # FPS, Frame Per Second
    # infinite loop bottom ----


# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE["width"], SCREEN_SIZE["height"]))
pygame.display.set_caption(TITLE)
screen.fill(BACKGROUND_COLOR)

# minecraft setup
mc = Minecraft.create(port=param.PORT_MC)
mc.postToChat(HELLO_MESSAGE)

create_frame()

main()
pygame.quit()
