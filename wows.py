import sys
import time
from random import randint

import pyautogui as pag
from pyautogui._window_win import getWindow

import settings as settings
from helper import get_battle_field_image, search_enemy_ships, select_nearest_enemy, distance, get_minimap_image, \
    search_template, get_map_image
from mouse import move_mouse

pag.PAUSE = 0
pag.FAILSAFE = False

NEED_MOVE = True
FIRE_ROUNDS = 0
MOVE_TO = None

SHIPS = [
    (138, 957),
    (138, 1024),
    # (138,1100),
]


def in_port():
    point = settings.SHIP_FILTER_BUTTON
    color = (148, 198, 199)
    result = pag.pixelMatchesColor(*point, color, tolerance=10)
    if result:
        check_battle_mode()
    return result


def select_ship():
    for loc in SHIPS:
        if pag.pixelMatchesColor(*loc,
                                 settings.SHIP_IN_BATTLE_COLOR,
                                 tolerance=20):
            print(f'skip {loc}')
            continue

        pag.moveTo(loc, duration=0.25)
        pag.click(clicks=3, interval=1, button='left')
        time.sleep(2)

        # print(f'Enter battle')
        pag.moveTo(settings.START_BUTTON, duration=0.25)
        pag.click(clicks=3, interval=0.5, button='left')

        if not in_port():
            break

    global NEED_MOVE
    NEED_MOVE = True


def quit_esc():
    if pag.pixelMatchesColor(*settings.QUIT_BATTLE_FINISHED_BUTTON2,
                             settings.BUTTON_COLOR,
                             tolerance=5):
        pag.press('esc')
        time.sleep(3)

    if pag.pixelMatchesColor(*settings.QUIT_BATTLE_FINISHED_BUTTON,
                             settings.BUTTON_COLOR,
                             tolerance=5):
        pag.press('esc')
        time.sleep(10)


def quit_battle():
    pag.press('esc')
    time.sleep(2)
    # print('quit_battle.click')
    pag.moveTo(settings.QUIT_BATTLE_BUTTON, duration=0.25)
    pag.click(clicks=2, interval=0.5, button='left')
    time.sleep(1)

    pag.moveTo(settings.QUIT_BATTLE_CONFIRM_BUTTON, duration=0.25)
    pag.click(clicks=2, interval=0.5, button='left')
    time.sleep(11)
    global NEED_MOVE
    NEED_MOVE = True


def in_battle():
    return pag.pixelMatchesColor(*settings.SHIP_TYPE_ICON,
                                 settings.BUTTON_COLOR,
                                 tolerance=5)


def is_alive():
    pix1 = pag.pixel(*settings.SPEED_S)
    pix2 = pag.pixel(*settings.SPEED_W)
    pix3 = pag.pixel(*settings.SPEED_M)
    result = sum([pag.pixelMatchesColor(*settings.SPEED_S, settings.BATTLE_SWM_COLOR, tolerance=50),
                  pag.pixelMatchesColor(*settings.SPEED_W, settings.BATTLE_SWM_COLOR, tolerance=50),
                  pag.pixelMatchesColor(*settings.SPEED_M, settings.BATTLE_SWM_COLOR, tolerance=50)]) > 1
    if not result:
        print('DEAD')
        print(pix1)
        print(pix2)
        print(pix3)
    return result


def move_ship():
    map_image = get_map_image()
    enemy_home = search_template(map_image, 'map_enemy_home.bmp')
    print(enemy_home)

    pag.press('m', presses=1, interval=0.25)
    time.sleep(1.5)
    for i in range(4):
        loc = (settings.MAP_CENTER[0] + randint(-90, 90),
               settings.MAP_CENTER[1] + randint(-90, 90))
        pag.moveTo(loc)
        pag.click(clicks=2, interval=0.5, button='left')
    time.sleep(1)
    pag.press('esc')
    time.sleep(2)


def start_battle():
    MOVE_TO = None
    pag.press('1')
    pag.press('y', presses=2, interval=0.25)
    pag.press('u', presses=2, interval=0.25)
    pag.sleep(1)

    move_ship2()

    # pag.moveTo(settings.MAP_CENTER)
    # pag.click(settings.MAP_CENTER, clicks=2)
    # pag.press('t', presses=1, interval=0.25)
    # pag.press('y', presses=1, interval=0.25)
    # pag.press('u', presses=1, interval=0.25)
    # pag.press('f10')

    global NEED_MOVE, FIRE_ROUNDS
    NEED_MOVE = False
    FIRE_ROUNDS = 0
    pag.sleep(20)


def focus_wows():
    wows_window = getWindow(settings.WINDOW_TITLE)
    # wows_window = getWindow('《战舰世界》')

    wows_window.restore()
    wows_window.set_position(*settings.WINDOW_POSITION)
    wows_window.set_foreground()  # switch to wows window

    # switch to port
    pag.moveTo(settings.PORT_BUTTON, duration=0.25)
    pag.click(clicks=2, interval=1, button='left')

def select_enemy():
    battle_field = get_battle_field_image()
    enemy_locs = []
    for ship_type in ['battle_blood']:
        enemy_locs += search_enemy_ships(battle_field, ship_type)
        if enemy_locs:
            break
    return select_nearest_enemy(enemy_locs)


def move_crosshair(loc):
    AIMING_OFFSET = (0, 60)
    x = loc[0] - settings.CROSSHAIR[0]
    y = (AIMING_OFFSET[1] + loc[1]) - settings.CROSSHAIR[1]

    print(settings.CROSSHAIR, '->', loc)
    print(x, y)
    move_mouse(x, y)


def fire_ship():
    if not pag.pixelMatchesColor(*settings.AUTO_PILOT,
                                 (76, 232, 170),
                                 tolerance=30):
        move_ship2()

    pag.press('`', presses=1, interval=0.25)
    pag.press('r', presses=1, interval=0.25)

    nearest_enemy_loc = select_enemy()
    # print(nearest_enemy_loc)

    if not nearest_enemy_loc:
        pag.sleep(10)
        return

    move_crosshair(nearest_enemy_loc)
    global FIRE_ROUNDS
    pag.sleep(2)

    # fire if gun is ready
    if pag.pixelMatchesColor(*settings.GUN_READY,
                             (30, 200, 120),
                             tolerance=30):
        pag.click(clicks=2, interval=0.25)

    pag.press('r', presses=1, interval=0.25)
    if not FIRE_ROUNDS % 10:
        # print(f'#{FIRE_ROUNDS} use consuption')
        pag.press('t', presses=1, interval=0.25)
        pag.press('y', presses=1, interval=0.25)
        pag.press('u', presses=1, interval=0.25)

    pag.sleep(1)
    FIRE_ROUNDS += 1


def check_battle_mode():
    if not pag.pixelMatchesColor(*settings.BATTLE_MODE,
                                 (14, 80, 79),
                                 tolerance=10):
        print('Please check battle mode.')
        sys.exit(0)


def move_ship2():
    global MOVE_TO
    pag.press('m', presses=1, interval=0.25)
    pag.sleep(2)
    pag.press('w', presses=5, interval=0.25)

    if not MOVE_TO:
        map_image = get_map_image()
        self_loc = search_template(map_image, 'map_friend_icon.bmp')
        print('self_loc', self_loc)

        if self_loc:
            MOVE_TO = (settings.BATTLE_MAP_TOPLEFT[0] + settings.BATTLE_MAP_SIZE[0] - self_loc[0],
                       settings.BATTLE_MAP_TOPLEFT[1] + settings.BATTLE_MAP_SIZE[1] - self_loc[1])
        else:
            MOVE_TO = (settings.BATTLE_MAP_TOPLEFT[0] + settings.BATTLE_MAP_SIZE[0] / 2,
                       settings.BATTLE_MAP_TOPLEFT[1] + settings.BATTLE_MAP_SIZE[1] / 2)

    for i in range(4):
        loc = (MOVE_TO[0] + randint(-50, 50),
               MOVE_TO[1] + randint(-50, 50))
        pag.moveTo(loc)
        pag.click(clicks=2, interval=0.5, button='left')

    time.sleep(1)
    pag.press('esc')
    time.sleep(2)


if __name__ == '__main__':
    focus_wows()
    quit_esc()

    while True:
        focus_wows()

        if in_battle():
            if is_alive():
                if NEED_MOVE:
                    print('In battle. alive')
                    start_battle()

                fire_ship()
            else:
                print('In battle. dead')
                quit_battle()
                continue
        elif in_port():
            print('In port.')
            select_ship()
        else:
            # print('In else, sleep 5 secs')
            time.sleep(5)
        quit_esc()
