import pyautogui as pag
import sys

pag.PAUSE = 0
pag.FAILSAFE = False
from helper import *
from wows import *
from mouse import *
import settings
from pyautogui._window_win import getWindow

BUTTON_FOLDER = 'buttons'
SHIP_FOLDER = 'ships'

ship1 = (174, 977)
start_button = (1182, 62)
QUIT_BUTTON_LOC = (1177, 514)

if __name__ == '__main__':
    wows_window = getWindow(settings.WINDOW_TITLE)
    wows_window.set_foreground()  # switch to wows window

    print(pag.pixel(1162, 606))
    print(pag.pixel(1162, 607))
    print(pag.pixel(1162, 605))
    print(pag.pixel(*settings.SPEED_S))
    print(pag.pixel(*settings.SPEED_W))
    print(pag.pixel(*settings.SPEED_M))
    while True:
        loc = select_enemy()
        print(loc)
        if loc:
            move_crosshair(loc)
            pag.click(settings.MAP_CENTER, clicks=2)
        pag.sleep(5)
        print('sleep 5')
    sys.exit(0)

    while True:
        nearest_enemy_loc = select_enemy()
        print(nearest_enemy_loc)
        if not nearest_enemy_loc:
            continue

        x = nearest_enemy_loc[0] - settings.CROSSHAIR[0]
        y = (60 + nearest_enemy_loc[1]) - settings.CROSSHAIR[1]
        print(x, y)
        # move_mouse(0,-150)
        move_crosshair(nearest_enemy_loc)
        # move_mouse(100,0)
        # if nearest_enemy_loc:
        # move_crosshair(nearest_enemy_loc)
