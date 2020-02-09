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
    (174,967),
    (174,1030),
    # (174,1100),
]
start_button=(1182,62)
QUIT_BUTTON_LOC=(1173,499)
QUIT_CONFIRM_BUTTON_LOC=(1097,611)
MAP_CENTER=(1131,567)
AIMING_CENTER=(1177,609)

need_move=True


def in_port():
    pix=pag.pixel(21,900)
    return pix==(148, 198, 199)
    # return pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'port_identifier.bmp'))

def select_ship():
    pag.click(start_button,clicks=1, button='left')
    for loc in SHIP_POINTS:
        pag.moveTo(loc)
        # print(f'Ship select {loc}')
        pag.click(loc, clicks=3, interval=1, button='left')
        pag.moveTo(start_button)
        # print(f'Enter battle')
        time.sleep(2)
        pag.click(start_button,clicks=2, interval=1, button='left')
    global need_move
    need_move=True

def quit_esc():
    if sum(pag.pixel(1170,1082)) > 250 * 3:
        pag.press('esc')
        time.sleep(3)
    if sum(pag.pixel(1168,1082)) > 250 * 3:
        pag.press('esc')
        time.sleep(10)

def quit_battle():
    pag.press('esc')
    time.sleep(1)
    # print('quit_battle.click')
    pag.click(QUIT_BUTTON_LOC, clicks=2, interval=1, button='left')
    time.sleep(1)
    pag.click(QUIT_CONFIRM_BUTTON_LOC, clicks=2, interval=1, button='left')
    time.sleep(11)
    global need_move
    need_move=True

def in_battle():
    return sum(pag.pixel(13,914)) > 230 * 3

def is_alive():
    if pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'ap.bmp')):
        return True
    if sum(pag.pixel(1268,612)) > 250 * 3:
        return True
        
    pix=pag.pixel(60,892)
    return pix[0]<35

def run_ship():
    pag.press('w', presses=5, interval=0.5)
    pag.press('1')
    pag.press('m')
    time.sleep(1)
    for i in range(4):
        loc=(MAP_CENTER[0]+randint(-90,90), MAP_CENTER[1]+randint(-90,90))
        pag.click(loc, clicks=2, interval=1, button='left')
    pag.press('esc')

    pag.click(loc,clicks=2)
    pag.press('t', presses=2, interval=0.5)
    pag.press('y', presses=2, interval=0.5)
    pag.press('u', presses=2, interval=0.5)
    global need_move
    need_move=False
    time.sleep(70)

def focus_wows():
    loc=(2190,119)
    pag.moveTo(loc)
    pag.click(loc,clicks=2, interval=1)

def print_pix(x,y):
    print(pag.pixel(x,y))

def fire_ship():
    pag.click(MAP_CENTER,clicks=2)
    pag.press('r', presses=2, interval=0.5)
    pag.press('t', presses=2, interval=0.5)
    pag.press('f3', presses=1)
    time.sleep(5)

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
        else:
            print('In else, sleep 5 secs')
            time.sleep(5)
        quit_esc()
