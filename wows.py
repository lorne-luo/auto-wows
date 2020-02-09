import time
from random import randint

import pyautogui as pag

pag.PAUSE = 0
pag.FAILSAFE = False

BUTTON_FOLDER = 'buttons'
NEED_MOVE = True

# in port, enter battle
WINDOW_FOCUS=(2190, 119)
SHIP_FILTER_BUTTON = (21, 900)  # in_port
START_BUTTON = (1182, 62)
# in battle
SHIP_TYPE_ICON = (13, 914)
AIMING_DISTANCE_KM = (1268, 612)
SHIP_HEALTH = (60, 892)
MAP_CENTER = (1131, 567)
AIMING_CENTER = (1177, 609)
# quit battle
QUIT_BATTLE_BUTTON = (1173, 499)
QUIT_BATTLE_CONFIRM_BUTTON = (1097, 611)
#  battle finished
QUIT_BATTLE_FINISHED_BUTTON = (1168, 1082)
QUIT_BATTLE_FINISHED_BUTTON2 = (1170, 1082)

SHIPS = [
    (174, 967),
    (174, 1030),
    # (174,1100),
]


def in_port():
    pix = pag.pixel(*SHIP_FILTER_BUTTON)
    return pix == (148, 198, 199)
    # return pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'port_identifier.bmp'))


def select_ship():
    for loc in SHIPS:
        # print(f'Ship select {loc}')
        pag.moveTo(loc)
        pag.click(loc, clicks=3, interval=1, button='left')

        # print(f'Enter battle')
        pag.moveTo(START_BUTTON)
        time.sleep(2)
        pag.click(START_BUTTON, clicks=2, interval=1, button='left')

        time.sleep(2)
        if not in_port():
            break

    global NEED_MOVE
    NEED_MOVE = True


def quit_esc():
    if sum(pag.pixel(*QUIT_BATTLE_FINISHED_BUTTON2)) > 250 * 3:
        pag.press('esc')
        time.sleep(3)
    if sum(pag.pixel(*QUIT_BATTLE_FINISHED_BUTTON)) > 250 * 3:
        pag.press('esc')
        time.sleep(10)


def quit_battle():
    pag.press('esc')
    time.sleep(1)
    # print('quit_battle.click')
    pag.click(QUIT_BATTLE_BUTTON, clicks=2, interval=1, button='left')
    time.sleep(1)
    pag.click(QUIT_BATTLE_CONFIRM_BUTTON, clicks=2, interval=1, button='left')
    time.sleep(11)
    global NEED_MOVE
    NEED_MOVE = True


def in_battle():
    return sum(pag.pixel(*SHIP_TYPE_ICON)) > 230 * 3


def is_alive():
    # if pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER, 'ap.bmp')):
    #     return True
    if sum(pag.pixel(*AIMING_DISTANCE_KM)) > 250 * 3:
        return True

    pix = pag.pixel(*SHIP_HEALTH)
    return pix[0] < 35


def move_ship():
    pag.press('m')
    time.sleep(1)
    for i in range(4):
        loc = (MAP_CENTER[0] + randint(-90, 90), MAP_CENTER[1] + randint(-90, 90))
        pag.click(loc, clicks=1, interval=1, button='left')
    pag.press('esc')


def start_battle():
    pag.press('w', presses=5, interval=0.5)
    pag.press('1')

    move_ship()

    pag.click(MAP_CENTER, clicks=2)
    pag.press('t', presses=1, interval=0.5)
    pag.press('y', presses=1, interval=0.5)
    pag.press('u', presses=1, interval=0.5)
    pag.press('f12')

    global NEED_MOVE
    NEED_MOVE = False
    time.sleep(60)


def focus_wows():
    pag.moveTo(WINDOW_FOCUS)
    pag.click(WINDOW_FOCUS, clicks=2, interval=1)


def print_pix(x, y):
    print(pag.pixel(x, y))


def fire_ship():
    pag.click(MAP_CENTER, clicks=2)
    pag.press('r', presses=1, interval=0.5)
    pag.press('t', presses=1, interval=0.5)
    pag.press('u', presses=1, interval=0.5)
    time.sleep(5)


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
