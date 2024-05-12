""" dot matrix display demo for pygame and minecraft
All in one, deluxe version.
"""
import os

# for pygame
import pygame
from pygame.colordict import THECOLORS as pg_colors
# see: https://www.pygame.org/docs/ref/color_list.html

# for minecraft
from mcje.minecraft import Minecraft
import param_MCJE as param

from dot_matrix import MatrixPG, MatrixMC, Scanner

if __name__ == "__main__":
    file_name = os.path.basename(__file__)
    dir_name = os.path.basename(os.path.dirname(__file__))
    HELLO_MESSAGE = 'hello!! this is ' + file_name + ' in the ' + dir_name + ' !!'

    # settings: pygame screen
    TITLE = HELLO_MESSAGE
    SCREEN_SIZE = {"width": 640, "height": 480}
    BACKGROUND_COLOR = pg_colors["lavender"]
    FPS = 60  # frames per second

    # settings: pygame key control
    KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL = 500, 50  # for pygame.key.set_repeat(), in mSec
    CTRL_X = {pygame.K_LEFT: -1, pygame.K_RIGHT: 1}
    CTRL_Y = {pygame.K_UP: -1, pygame.K_DOWN: 1}
    CTRL_COLOR = {pygame.K_1: "red",
                  pygame.K_2: "green",
                  pygame.K_3: "blue",
                  pygame.K_4: "yellow",
                  pygame.K_5: "orange",
                  pygame.K_6: "purple"}

    # settings: pygame -> minecraft color mapping
    MC_COLORS = {"red": "RED_WOOL",
                 "green": "LIME_WOOL",
                 "blue": "BLUE_WOOL",
                 "yellow": "YELLOW_WOOL",
                 "orange": "ORANGE_WOOL",
                 "purple": "PURPLE_WOOL"}

    def init_setup():
        # pygame setup
        pygame.init()
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)

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
        matrix3 = MatrixMC(mc=mc, m=9, n=5,
                           colors={"on": "GOLD_BLOCK",
                                   "off": "IRON_BLOCK",
                                   "frame": "SEA_LANTERN_BLOCK",
                                   "background": "AIR"},
                           with_frame=True,
                           x0=-10, y0=param.Y_SEA + 25, z0=18)
        matrix4 = MatrixMC(mc=mc, m=19, n=8,
                           colors={"on": "RED_WOOL",
                                   "off": "SEA_LANTERN_BLOCK",
                                   "frame": "IRON_BLOCK",
                                   "background": "AIR"},
                           with_frame=False,
                           x0=10, y0=param.Y_SEA + 15, z0=20)

        matrices = [matrix1, matrix2, matrix3, matrix4]
        scanners = [Scanner(matrices[0], pos=[0, 0], change=[-1, -1], wait=0.2, direction="vertical"),
                    Scanner(matrices[1], pos=[0, 0], change=[1, 1], wait=0.1, direction="control"),
                    Scanner(matrices[2], pos=[0, 0], change=[1, -1], wait=0.3, direction="horizontal"),
                    Scanner(matrices[3], pos=[0, 0], change=[-1, -1], wait=0.1, direction="control")]

        return matrices, scanners

    def check_keys(event):
        x_change, y_change = 0, 0
        color = None
        update_flag = False
        update_color_flag = False
        if event.type == pygame.KEYDOWN:
            if event.key in CTRL_X:
                x_change = CTRL_X[event.key]
                update_flag = True
            if event.key in CTRL_Y:
                y_change = CTRL_Y[event.key]
                update_flag = True
            if event.key in CTRL_COLOR:
                color = CTRL_COLOR[event.key]
                update_color_flag = True
        if event.type == pygame.KEYUP:
            if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                x_change = 0
                update_flag = True
            if event.key in {pygame.K_UP, pygame.K_DOWN}:
                y_change = 0
                update_flag = True
        return x_change, y_change, color, update_flag, update_color_flag

    def update_matrices(matrices, scanners, skip_frames, x_change, y_change, color, update_flag, update_color_flag):
        for i, matrix in enumerate(matrices):
            if scanners[i].direction == "control":
                if update_color_flag:
                    if matrix.output == "minecraft":
                        color = MC_COLORS[color]
                    matrix.colors["on"] = color
                    scanners[i].tick()
                if update_flag:
                    scanners[i].set_change(change=(x_change, y_change))
                    scanners[i].tick()
            elif skip_frames[i] > FPS * scanners[i].wait:
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
                # key control
                x_change, y_change, color, update_flag, update_color_flag = check_keys(event)

            # update_matrices
            update_matrices(matrices, scanners, skip_frames, x_change, y_change, color, update_flag, update_color_flag)

            update_flag = False
            update_color_flag = False
            clock.tick(FPS)  # FPS, Frame Per Second
        # infinite loop bottom ----

    main(init_setup())
    pygame.quit()
