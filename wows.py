import time
from random import randint

import pyautogui as pag
from pyautogui._window_win import getWindow

import settings as settings
from helper import get_battle_field_image, search_enemy_ships, select_nearest_enemy, distance
from mouse import move_mouse

pag.PAUSE = 0
pag.FAILSAFE = False

NEED_MOVE = True
FIRE_ROUNDS = 0

SHIPS = [
    (174, 967),
    (174, 1030),
    # (174,1100),
]


def in_port():
    point = settings.SHIP_FILTER_BUTTON
    color = (148, 198, 199)
    return pag.pixelMatchesColor(*point, color, tolerance=10)


def select_ship():
    for loc in SHIPS:
        # print(f'Ship select {loc}')
        pag.moveTo(loc, duration=0.25)
        pag.click(loc, clicks=3, interval=1, button='left')
        time.sleep(2)

        # print(f'Enter battle')
        pag.moveTo(settings.START_BUTTON, duration=0.25)
        pag.click(settings.START_BUTTON, clicks=3, interval=0.5, button='left')
        time.sleep(2)

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
    pag.click(settings.QUIT_BATTLE_BUTTON, clicks=2, interval=0.5, button='left')
    time.sleep(1)

    pag.moveTo(settings.QUIT_BATTLE_CONFIRM_BUTTON, duration=0.25)
    pag.click(settings.QUIT_BATTLE_CONFIRM_BUTTON, clicks=2, interval=0.5, button='left')
    time.sleep(11)
    global NEED_MOVE
    NEED_MOVE = True


def in_battle():
    return pag.pixelMatchesColor(*settings.SHIP_TYPE_ICON,
                                 settings.BUTTON_COLOR,
                                 tolerance=5)


def is_alive():
    return all([pag.pixelMatchesColor(*settings.SPEED_S, settings.BUTTON_COLOR, tolerance=50),
                pag.pixelMatchesColor(*settings.SPEED_W, settings.BUTTON_COLOR, tolerance=50),
                pag.pixelMatchesColor(*settings.SPEED_M, settings.BUTTON_COLOR, tolerance=50)])


def move_ship():
    pag.press('m', presses=2, interval=0.25)
    time.sleep(1)
    for i in range(4):
        loc = (settings.MAP_CENTER[0] + randint(-90, 90),
               settings.MAP_CENTER[1] + randint(-90, 90))
        pag.moveTo(loc)
        pag.click(loc, clicks=2, interval=0.25, button='left')
    pag.press('esc')
    time.sleep(1)


def start_battle():
    pag.press('width', presses=5, interval=0.25)
    pag.press('1')

    move_ship()

    pag.moveTo(settings.MAP_CENTER)
    pag.click(settings.MAP_CENTER, clicks=2)
    pag.press('t', presses=1, interval=0.25)
    pag.press('y', presses=1, interval=0.25)
    pag.press('u', presses=1, interval=0.25)
    pag.press('f10')

    global NEED_MOVE, FIRE_ROUNDS
    NEED_MOVE = False
    FIRE_ROUNDS = 0
    time.sleep(70)


def focus_wows():
    wows_window = getWindow(settings.WINDOW_TITLE)
    # wows_window = getWindow('《战舰世界》')

    wows_window.set_position(*settings.WINDOW_POSITION)
    wows_window.set_foreground()  # switch to wows window


def select_enemy():
    battle_field = get_battle_field_image()
    enemy_locs = []
    for ship_type in ['dd', 'ca', 'bb']:
        enemy_locs += search_enemy_ships(battle_field, ship_type)
        if enemy_locs:
            break
    return select_nearest_enemy(enemy_locs)


def move_crosshair(loc):
    AIMING_OFFSET = (0, 60)
    x = loc[0]-settings.CROSSHAIR[0]
    y =(AIMING_OFFSET[1] + loc[1])- settings.CROSSHAIR[1]

    # print(settings.CROSSHAIR,'->',loc)
    # print(x,y)
    move_mouse(x, y)

    dis = distance(AIMING_OFFSET, loc)
    seconds = dis / 1000 * 15
    pag.sleep(seconds )


def fire_ship():
    nearest_enemy_loc = select_enemy()
    print(nearest_enemy_loc)

    if not nearest_enemy_loc:
        pag.sleep(10)
        return

    move_crosshair(nearest_enemy_loc)
    global FIRE_ROUNDS

    # pag.press('shiftleft', presses=2, interval=0.25)
    pag.click(settings.MAP_CENTER, clicks=2)
    pag.press('r', presses=1, interval=0.25)
    if not FIRE_ROUNDS % 10:
        pag.press('t', presses=1, interval=0.25)
        pag.press('y', presses=1, interval=0.25)
        pag.press('u', presses=1, interval=0.25)
    pag.sleep(1)
    # pag.press('shiftleft', presses=1, interval=0.25)

    time.sleep(5)
    pag.click(settings.MAP_CENTER, clicks=2)
    FIRE_ROUNDS += 1


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
            print('In else, sleep 5 secs')
            time.sleep(5)
        quit_esc()
