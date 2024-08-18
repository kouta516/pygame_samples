# demo for handmade LCD font

import pygame
import pygame.freetype
# import time
from lcd_font_pg import LCD_font

DARK_GRAY = (40, 40, 40)
GRAY = (80, 80, 80)
RED = (255, 0, 0)
GREEN = (10, 250, 10)
CYAN = (120, 120, 250)
YELLOW = (250, 250, 20)
WHITE = (250, 250, 250)

WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("LCD font")

clock = pygame.time.Clock()

font1 = pygame.freetype.Font("fonts/natumemozi.ttf", 48)

lcd1 = LCD_font(screen)
lcd1.init_col(BLOCK_SIZE=7, BLOCK_INTV=8, COLOR_ON=GREEN, COLOR_OFF=GRAY)
lcd1.init_row(X_ORG=8, Y_ORG=8, COL_INTV=6)


def LCD_display(x, y):
    code = int((x / 8) % 10)
    text1, rect1 = font1.render(str(code), WHITE)
    rect1.center = (x, y)
    screen.blit(text1, rect1)
    # LCD sim
    lcd1.update_col(col=0, code=code)
    lcd1.update_col(col=2, code=(code + 2) % 10)
    lcd1.update_col(col=3, code=(code + 3) % 10)


def infinite_loop():
    x = WINDOW_WIDTH * 0.5
    y = WINDOW_HEIGHT * 0.5

    x_change = 0
    y_change = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -1
                if event.key == pygame.K_RIGHT:
                    x_change = 1
                if event.key == pygame.K_UP:
                    y_change = -1
                if event.key == pygame.K_DOWN:
                    y_change = 1

            if event.type == pygame.KEYUP:
                if (
                    event.key == pygame.K_LEFT
                    or event.key == pygame.K_RIGHT
                    or event.key == pygame.K_UP
                    or event.key == pygame.K_DOWN
                ):
                    x_change = 0
                    y_change = 0

        x += x_change
        y += y_change

        if x > WINDOW_WIDTH:
            x = WINDOW_WIDTH
        if y > WINDOW_HEIGHT:
            y = WINDOW_HEIGHT
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        screen.fill(GRAY)
        LCD_display(x, y)

        pygame.display.update()
        clock.tick(60)


infinite_loop()
pygame.quit()
