# demo for 7-segment simulation
# using the class 'Seven_seg' in seven_seg_pg.py

from datetime import datetime
import pygame
from seven_seg_pg import Seven_seg
from lcd_font_pg import LCD_font


DARK_GRAY = (40, 40, 40)
GRAY = (80, 80, 80)
RED = (255, 0, 0)
GREEN = (10, 250, 10)
CYAN = (120, 120, 250)
YELLOW = (250, 250, 20)
WHITE = (250, 250, 250)

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([480, 320])
pygame.display.set_caption("pygame 7-segment display simulation")
screen.fill(DARK_GRAY)

display5 = Seven_seg(screen)
display5.init_col(BLOCK_SIZE=9, BLOCK_INTV=9, COLOR_ON=(120, 200, 250), COLOR_OFF=GRAY)
display5.init_row(X_ORG=8, Y_ORG=8, COL_INTV=6)

display6 = LCD_font(screen)
display6.init_col(BLOCK_SIZE=4, BLOCK_INTV=6, COLOR_ON=WHITE, COLOR_OFF=GRAY)
display6.init_row(X_ORG=10, Y_ORG=21, COL_INTV=6)

display7 = LCD_font(screen)
display7.init_col(BLOCK_SIZE=6, BLOCK_INTV=8, COLOR_ON=RED, COLOR_OFF=GRAY)
display7.init_row(X_ORG=6, Y_ORG=24, COL_INTV=6)

running = True
# infinite loop top ----
while running:
    for count in range(16 ** 4):  # 0から65535まで
        # press ctrl-c or close the window to stop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not running:
            break
        # 「for count」のループから抜ける。whileループも抜ける。

        dt_now = datetime.now()
        time_now = (dt_now.hour * 10000
                    + dt_now.minute * 100
                    + dt_now.second)
        display5.disp_num2(zfil=True, rjust=6, num=time_now, base=10)

        display6.update_col(col=0, code=int(str(dt_now.year)[0]))
        display6.update_col(col=1, code=int(str(dt_now.year)[1]))
        display6.update_col(col=2, code=int(str(dt_now.year)[2]))
        display6.update_col(col=3, code=int(str(dt_now.year)[3]))
        display6.update_col(col=4, code=11)
        display6.update_col(col=5, code=dt_now.month // 10)
        display6.update_col(col=6, code=dt_now.month % 10)
        display6.update_col(col=7, code=11)
        display6.update_col(col=8, code=dt_now.day // 10)
        display6.update_col(col=9, code=dt_now.day % 10)

        display7.update_col(col=0, code=dt_now.hour // 10)
        display7.update_col(col=1, code=dt_now.hour % 10)
        display7.update_col(col=2, code=10)
        display7.update_col(col=3, code=dt_now.minute // 10)
        display7.update_col(col=4, code=dt_now.minute % 10)
        display7.update_col(col=5, code=10)
        display7.update_col(col=6, code=dt_now.second // 10)
        display7.update_col(col=7, code=dt_now.second % 10)

        pygame.display.flip()  # update_col
        clock.tick(20)  # FPS, Frame Per Second
    screen.fill(DARK_GRAY)
# infinit loop bottom ----

pygame.quit()
