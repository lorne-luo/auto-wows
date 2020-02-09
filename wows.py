import os
import sys
import time

import pyautogui as pag
from random import randint

pag.PAUSE = 0
pag.FAILSAFE=False

BUTTON_FOLDER = 'buttons'
SHIP_FOLDER = 'ships'
SHIP_POINTS=[
    (174,977),
    (174,1050),
]
start_button=(1182,62)
QUIT_BUTTON_LOC=(1177,514)
QUIT_CONFIRM_BUTTON_LOC=(1097,626)
MAP_CENTER=(1181,567)
need_move=True


def in_port():
    pix=pag.pixel(22,1173)
    return pix==(243, 214, 191)


def select_ship():
    for loc in SHIP_POINTS:
        pag.moveTo(loc)
        print(f'Ship select {loc}')
        pag.click(loc, clicks=3, interval=1, button='left')
        pag.moveTo(start_button)
        print(f'Enter battle')
        time.sleep(2)
        pag.click(start_button,clicks=3, interval=1, button='left')
    global need_move
    need_move=True

def is_battle_finish():
    return pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'battle_finish_identifier.bmp'))

def quit_esc():
    if sum(pag.pixel(1168,1109)) > 230 * 3:
        pag.press('esc')
        time.sleep(3)
    if sum(pag.pixel(1146,1104)) > 230 * 3:
        pag.press('esc')
        time.sleep(7)

def quit_battle():
    pag.press('esc')
    time.sleep(1)
    print('quit_battle.click')
    pag.click(QUIT_BUTTON_LOC, clicks=2, interval=1, button='left')
    time.sleep(1)
    pag.click(QUIT_CONFIRM_BUTTON_LOC, clicks=2, interval=1, button='left')
    time.sleep(11)
    global need_move
    need_move=True

def in_battle():
    return sum(pag.pixel(11,937)) > 230 * 3

def is_alive():
    pix=pag.pixel(1076,1142)
    print('is alive',pix)
    return pix==(183, 31, 6) or pix == (146, 46, 14)

def run_ship():
    pag.press('w', presses=5, interval=0.5)
    pag.press('m')
    time.sleep(1)
    for i in range(4):
        loc=(MAP_CENTER[0]+randint(-90,90), MAP_CENTER[1]+randint(-90,90))
        pag.click(loc, clicks=2, interval=1, button='left')
    pag.press('esc')

    pag.click(loc,clicks=2)
    pag.press('y', presses=2, interval=0.5)
    pag.press('r', presses=2, interval=0.5)
    global need_move
    need_move=False
    time.sleep(70)

def focus_wows():
    loc=(79,14)
    pag.moveTo(loc)
    pag.click(loc,clicks=2, interval=1)

def print_pix(x,y):
    print(pag.pixel(x,y))

def fire_ship():
    pag.click(MAP_CENTER,clicks=2)
    pag.press('r', presses=2, interval=0.5)
    pag.press('f3', presses=1)


if __name__ == '__main__':


    # loc =  pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'ap.bmp'))
    # loc=in_port()
    # print('#',loc)
    # print_pix(11,937)
    # pag.click(70,14)
    # quit_esc()
    # sys.exit(0)

    while True:
        focus_wows()
        quit_esc()
        if in_battle():
            if is_alive():
                if need_move:
                    print('In battle. alive')
                    run_ship()
                fire_ship()
            else:
                print('In battle. dead')
                quit_battle()
                continue
        elif in_port():
            print('In port.')
            select_ship()

        # elif is_battle_finish():
        #     print('Battle finished.')
        #     quit_battle()
        else:
            print('In else, sleep 5 secs')
            time.sleep(15)

        quit_esc()
