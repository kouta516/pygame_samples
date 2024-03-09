"""LCD font monthly calendar with changeable month and year
"""
from datetime import datetime
from datetime import date
import pygame
from pygame.colordict import THECOLORS as pg_colors
from lcd_font_pg import LCD_font as LCD_font_pg

# color names are defined in pygame.colordict.THECOLORS
# https://www.pygame.org/docs/ref/color_list.html

FPS = 30  # frames per second, 15 is enough and over 60 is not necessary
WAIT = 0.15  # wait for the next key press in seconds
KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL = 500, 250  # for pygame.key.set_repeat()
WIDTH, HEIGHT = 670, 480
TITLE = "LCD font monthly calendar"
# 文字色と背景色の設定
COLOR = pg_colors['firebrick4']
BACKGROUND = pg_colors['lightblue2']
# 年と月の変更、「今日」のためのキー設定
CTRL_KEYS = [[pygame.K_UP, "YEAR", 1],
             [pygame.K_DOWN, "YEAR", -1],
             [pygame.K_LEFT, "MONTH", -1],
             [pygame.K_RIGHT, "MONTH", 1],
             [pygame.K_t, "TODAY", '']]
# 日曜始まり、月曜始まりの設定
FIRST_DAY_OF_WEEK = 1  # 0:Sunday, 1:Monday


def init_display():
    """initialize the screen and font style"""
    pygame.init()
    pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption(TITLE)
    screen.fill(BACKGROUND)

    lcd1 = LCD_font_pg(screen)
    lcd1.init_col(BLOCK_SIZE=6, BLOCK_INTV=7, COLOR_ON=COLOR, COLOR_OFF=BACKGROUND)
    lcd1.init_row(X_ORG=4, Y_ORG=4, COL_INTV=6)

    lcd2 = LCD_font_pg(screen)
    lcd2.init_col(BLOCK_SIZE=4, BLOCK_INTV=5, COLOR_ON=COLOR, COLOR_OFF=BACKGROUND)
    lcd2.init_row(X_ORG=10, Y_ORG=22, COL_INTV=18)

    lcdx = LCD_font_pg(screen)
    lcdx.init_col(BLOCK_SIZE=4, BLOCK_INTV=5, COLOR_ON=COLOR, COLOR_OFF=BACKGROUND)

    return (lcd1, lcd2, lcdx, screen)


def get_month_days(y, m):
    """その月の日数を取得する。"""
    if m in {1, 3, 5, 7, 8, 10, 12}:
        days = 31
    elif m in {4, 6, 9, 11}:
        days = 30
    elif m == 2:
        if y % 4 == 0 and y % 100 != 0 or y % 400 == 0:
            days = 29
        days = 28
    else:
        days = 0  # error
    return days


def get_week_day(y, m, d):
    """ツェラーの公式により曜日を求める。
    日曜日が0、月曜日が1、・・・、土曜日が6に対応する。
    y: 年, m: 月, d: 日
    """
    if m in {1, 2}:
        y -= 1
        m += 12
    w = (y + y // 4 - y // 100 + y // 400 + (13 * m + 8) // 5 + d) % 7
    return w


def get_week_day2(y, m, d):
    """datetime.date(y, m, d).weekday()で求めることもできる。
    この場合、月曜日が0、火曜日が1、・・・、日曜日が6に対応する。
    コード全体で、「月曜が0」前提にするとスッキリする。
    """
    # return date(y, m, d).weekday()  # 「月曜が0」前提のとき
    return (date(y, m, d).weekday() + 1) % 7  # 「日曜が0」前提なので、調整。


def update_month(display, y, m):
    """
    y:年, m:月のカレンダーをlcdxに表示する。
    年-月-日-曜日の表示lcd1を更新する。
    曜日行のlcd2を更新する。
    """
    lcd1, lcd2, lcdx, screen = display
    screen.fill(BACKGROUND)  # clear the screen buffer
    for i in range(7):
        lcd2.update_col(col=i, code=13 + (i + FIRST_DAY_OF_WEEK) % 7)  # 曜日行表示

    # 年-月-日-曜日の表示
    lcd1.update_col(col=0, code=int(str(y)[0]))
    lcd1.update_col(col=1, code=int(str(y)[1]))
    lcd1.update_col(col=2, code=int(str(y)[2]))
    lcd1.update_col(col=3, code=int(str(y)[3]))
    lcd1.update_col(col=4, code=12)  # ハイフン
    if m // 10 != 0:
        lcd1.update_col(col=5, code=m // 10)
    lcd1.update_col(col=6, code=m % 10)  # 月

    wd = get_week_day2(y, m, 1)
    wd = (wd - FIRST_DAY_OF_WEEK) % 7
    z = get_month_days(y, m)

    for n in range(z):  # nはcol2行分で各日にちを表し、各月の日数分であるｚ回繰り返して日付表示する
        x = 3 + ((3 * n + 2) + wd * 3) // 21
        lcdx.init_row(X_ORG=1, Y_ORG=(12 + (x - 1) * 10), COL_INTV=6)
        if ((n + 1) // 10) != 0:
            lcdx.update_col(col=((3 * n + 1) + wd * 3) % 21, code=(n + 1) // 10)  # カレンダー各日10の位
        lcdx.update_col(col=((3 * n + 2) + wd * 3) % 21, code=(n + 1) % 10)  # カレンダー各日1の位

    pygame.display.flip()  # update the screen with buffer


def main(display):
    """main routine"""
    the_year = 0
    the_month = 0
    clock = pygame.time.Clock()

    # 最初に、今月のカレンダーを表示
    dt_now = datetime.now()
    the_year = dt_now.year
    the_month = dt_now.month
    update_flag = True

    y_change = 0
    m_change = 0
    skip_frames = FPS * WAIT + 1
    running = True

    # infinite loop top ----
    while running:
        # press ctrl-c or close the window to stop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                for key in CTRL_KEYS:
                    if event.key == key[0]:
                        if key[1] == "YEAR":
                            y_change = key[2]
                            update_flag = True
                        elif key[1] == "MONTH":
                            m_change = key[2]
                            update_flag = True
                        elif key[1] == "TODAY":
                            the_year = dt_now.year
                            the_month = dt_now.month
                            y_change = 0
                            m_change = 0
                            update_flag = True
            elif event.type == pygame.KEYUP:
                for key in CTRL_KEYS:
                    if event.key == key[0]:
                        if key[1] == "YEAR":
                            y_change = 0
                        elif key[1] == "MONTH":
                            m_change = 0

        if update_flag and (skip_frames > FPS * WAIT):
            update_flag = False
            skip_frames = 0
            the_year += y_change
            the_month += m_change
            if the_month > 12:
                the_month = 1
                the_year += 1
            elif the_month < 1:
                the_month = 12
                the_year -= 1
            update_month(display, the_year, the_month)

        skip_frames += 1
        clock.tick(FPS)  # FPS, Frame Per Second
    # infinite loop bottom ----


# main routine
main(init_display())  # initialize screen and start the main routine
pygame.quit()
