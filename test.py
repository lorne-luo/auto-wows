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
    wows_window.restore()
    wows_window.set_foreground()  # switch to wows window
    pag.sleep(1)

    move_ship2()

    sys.exit(0)

    pag.press('m', presses=1, interval=0.25)
    pag.sleep(1.5)

    map_image = get_map_image()
    enemy_home = search_teamplate(map_image, 'map_enemy_home.bmp')
    print('enemy_home', enemy_home)

    self_loc = search_teamplate(map_image, 'map_self_icon.bmp')
    print('map_self_icon', self_loc)

    if not enemy_home:
        loc = (settings.BATTLE_MAP_TOPLEFT[0] + enemy_home[0],
               settings.BATTLE_MAP_TOPLEFT[1] + enemy_home[1])
        pag.click(loc, clicks=2, interval=0.5, button='left')
    else:
        self_loc = search_teamplate(map_image, 'map_self_icon.bmp')
        print('map_self_icon', self_loc)
        loc = (settings.BATTLE_MAP_TOPLEFT[0] + settings.BATTLE_MAP_SIZE[0] - self_loc[0],
               settings.BATTLE_MAP_TOPLEFT[1] + settings.BATTLE_MAP_SIZE[1] - self_loc[1])
        pag.click(loc, clicks=2, interval=0.5, button='left')

    time.sleep(1)
    pag.press('esc')

    # check_battle_mode()

    # print(pag.pixel(1284, 63))
    # print(pag.pixel(1162, 605))
    # print(is_alive())
    # print(pag.pixel(*settings.SPEED_S))
    # print(pag.pixel(*settings.SPEED_W))
    # print(pag.pixel(*settings.SPEED_M))
    sys.exit(0)

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
