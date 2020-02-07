import os
import time

import pyautogui as pag

pag.PAUSE = 1

BUTTON_FOLDER = 'buttons'
SHIP_FOLDER = 'ships'
SHIP_POINTS=[
    (174,977),
    (174,1050)
]
start_button=(1182,62)
QUIT_BUTTON_LOC=(1177,514)

def in_port():
    loc = pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'port_identifier.bmp'))
    return loc


def select_ship():
    for loc in SHIP_POINTS:
        pag.moveTo(loc)
        pag.click(loc, clicks=2, interval=1, button='left')
        pag.moveTo(start_button)
        pag.click(start_button,clicks=2, interval=1, button='left')

def is_battle_finish():
    return pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'battle_finish_identifier.bmp'))


def quit_battle_menu():
    loc = pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'quit_battle_button.png'))
    if not loc:
        return

    pag.click(x=loc.x, y=loc.y, clicks=2, interval=0.5, button='left')

def quit_esc():
    pics=['back_game.bmp','back_port.bmp','close.bmp']
    for pic in pics:
        loc = pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,pic))
        if loc:
            pag.moveTo(loc)
            pag.click(loc,clicks=2, interval=2, button='left')
            # pag.press('esc')

def quit_battle():
    quit_esc()
    loc = pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'quit_battle_button.bmp'))
    if loc:
        # quit button already here

        pag.click(x=loc.x, y=loc.y, clicks=2, interval=1, button='left')
    else:
        quit_esc()
        pag.press('esc')
        pag.click(QUIT_BUTTON_LOC, clicks=2, interval=1, button='left')

    quit_esc()

    loc = pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'quit_battle_button.png'))
    if not loc:
        return

    pag.click(x=loc.x, y=loc.y, clicks=2, interval=1, button='left')


def in_battle():
    point=(2332,1168)
    pix=pag.pixel(*point)
    result = pix in [(16, 60, 89) ,(3, 45, 33),(27, 31, 39),(34, 62, 63),(10, 40, 50)]
    if not result:
        print(pix)
    return result
def is_dead():
    result= not pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'sunguan.bmp'))
    if result:
        print('dead')
    return result

def run_ship():
    pag.press('w', presses=5, interval=0.5)

while True:
    pag.click(70,14)
    quit_esc()

    if in_port():
        print('In port.')
        select_ship()
    elif in_battle():
        print('In battle.')
        if check_dead():
            quit_battle()
        else:
            run_ship()
    elif is_battle_finish():
        print('Battle finished.')
        quit_battle()
    else:
        print('In else.')
