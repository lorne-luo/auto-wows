import time
from random import randint

import pyautogui as pag

import settings as settings

pag.PAUSE = 0
pag.FAILSAFE = False

NEED_MOVE = True

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
        pag.moveTo(loc, duration=0.5)
        pag.click(loc, clicks=3, interval=1, button='left')
        time.sleep(2)

        # print(f'Enter battle')
        pag.moveTo(settings.START_BUTTON, duration=0.5)
        pag.click(settings.START_BUTTON, clicks=3, interval=1, button='left')
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
    pag.moveTo(settings.QUIT_BATTLE_BUTTON, duration=0.5)
    pag.click(settings.QUIT_BATTLE_BUTTON, clicks=2, interval=1, button='left')
    time.sleep(1)

    pag.moveTo(settings.QUIT_BATTLE_CONFIRM_BUTTON, duration=0.5)
    pag.click(settings.QUIT_BATTLE_CONFIRM_BUTTON, clicks=2, interval=1, button='left')
    time.sleep(11)
    global NEED_MOVE
    NEED_MOVE = True


def in_battle():
    return pag.pixelMatchesColor(*settings.SHIP_TYPE_ICON,
                                 settings.BUTTON_COLOR,
                                 tolerance=5)


def is_alive():
    if pag.pixelMatchesColor(*settings.AIMING_DISTANCE_KM,
                                 settings.BUTTON_COLOR,
                                 tolerance=5):
        return True

    # todo this may wrong
    pix = pag.pixel(*settings.SHIP_HEALTH)
    return pix[0] < 35


def move_ship():
    pag.press('m')
    time.sleep(1)
    for i in range(4):
        loc = (settings.MAP_CENTER[0] + randint(-90, 90),
               settings.MAP_CENTER[1] + randint(-90, 90))
        pag.moveTo(loc)
        pag.click(loc, clicks=2, interval=0.5, button='left')
    pag.press('esc')
    time.sleep(1)


def start_battle():
    pag.press('w', presses=5, interval=0.5)
    pag.press('1')

    move_ship()

    pag.moveTo(settings.MAP_CENTER, duration=0.5)
    pag.click(settings.MAP_CENTER, clicks=2)
    pag.press('t', presses=1, interval=0.5)
    pag.press('y', presses=1, interval=0.5)
    pag.press('u', presses=1, interval=0.5)
    pag.press('f10')

    global NEED_MOVE
    NEED_MOVE = False
    time.sleep(60)


def focus_wows():
    pag.click(settings.WINDOW_FOCUS, clicks=2, interval=1)


def print_pix(x, y):
    print(pag.pixel(x, y))


def fire_ship():
    pag.click(settings.MAP_CENTER, clicks=2)
    pag.press('r', presses=1, interval=0.5)
    pag.press('t', presses=1, interval=0.5)
    pag.press('u', presses=1, interval=0.5)
    time.sleep(5)
    # move_turret = (randint(-300, 300), randint(-20, 20))
    # print(f'Move turret {move_turret}')
    # pag.move(*move_turret, duration=0.5)


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
