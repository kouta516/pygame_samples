'''
moving dot demo in pygame
'''
import pygame

# settings for pygame
ON_PG = WHITE = (255, 255, 255)
OFF_PG = HOT_PINK = (255, 105, 180)
BACK_PG = DARK_GRAY = (64, 64, 64)
dot_size = 10
dot_intv = 12
width, height = dot_size, dot_size
x0_pg, y0_pg = 5, 5

# initialization for pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([480, 320])
pygame.display.set_caption("hello, world!")
screen.fill(BACK_PG)

# clear field in pygame
for x in range(5):
    for y in range(7):
        left, top = (x0_pg + x) * dot_intv, (y0_pg + y) * dot_intv
        pygame.draw.rect(screen, OFF_PG, (left, top, width, height))


# infinite loop top ----
x, y = 0, 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # erase the previous dot in pygame
    left, top = (x0_pg + x) * dot_intv, (y0_pg + y) * dot_intv
    pygame.draw.rect(screen, OFF_PG, (left, top, width, height))

    # update the current dot position
    x += 1
    if x == 5:  # 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, ...
        x = 0
        y += 1
        if y == 7:  # 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, ...
            y = 0
    print(x, y)

    # draw the current dot in pygame
    left, top = (x0_pg + x) * dot_intv, (y0_pg + y) * dot_intv
    pygame.draw.rect(screen, ON_PG, (left, top, width, height))

    pygame.display.flip()
    clock.tick(3)  # FPS, Frame Per Second

pygame.quit()
