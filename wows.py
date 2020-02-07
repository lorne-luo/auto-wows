import os
import time

import pyautogui as pag

pag.PAUSE = 1

BUTTON_FOLDER = 'buttons'
SHIP_FOLDER = 'ships'


def in_port():
    loc = pag.locateCenterOnScreen(f'{BUTTON_FOLDER}/battle_start_button.png')
    return loc


def select_ship():
    file_names = os.listdir(SHIP_FOLDER)
    for filename in file_names:
        if filename.endswith('png'):
            loc = pag.locateCenterOnScreen(f'{SHIP_FOLDER}/{filename}')
            if loc:
                pag.click(x=loc.x, y=loc.y, clicks=2, interval=1, button='left')
                break


def start_battle(loc):
    if loc:
        pag.click(x=loc.x, y=loc.y, clicks=3, interval=0.5, button='left')


def is_battle_finish():
    return pag.locateCenterOnScreen(f'{BUTTON_FOLDER}/battle_finish_identifier.png')


def quit_battle_menu():
    loc = pag.locateCenterOnScreen(f'{BUTTON_FOLDER}/quit_battle_button.png')
    if not loc:
        return

    pag.click(x=loc.x, y=loc.y, clicks=2, interval=0.5, button='left')


def quit_esc():
    loc = pag.locateCenterOnScreen(f'{BUTTON_FOLDER}/esc.png')
    while loc:
        pag.click(x=loc.x, y=loc.y)
        pag.press('esc')
        loc = pag.locateCenterOnScreen(f'{BUTTON_FOLDER}/esc.png')


def quit_battle():
    quit_esc()

    if not pag.locateCenterOnScreen(f'{BUTTON_FOLDER}/battle_identifier.png'):
        # not in battle
        return

    locations = pag.locateCenterOnScreen(f'{BUTTON_FOLDER}/quit_battle_button.png')
    if locations:
        # quit button already here
        left, right, width, height = locations[0]
        pag.click(x=left, y=right, clicks=2, interval=1, button='left')
    else:
        quit_esc()
        pag.press('esc')
        locations = pag.locateCenterOnScreen(f'{BUTTON_FOLDER}/quit_battle_button.png')
        if locations:
            left, right, width, height = locations[0]
            pag.click(x=left, y=right, clicks=2, interval=1, button='left')

    quit_esc()

    locations = pag.locateCenterOnScreen(f'{BUTTON_FOLDER}/quit_battle_button.png')
    if not locations:
        return

    left, right, width, height = locations[0]
    pag.click(x=left, y=right, clicks=2, interval=1, button='left')


def in_battle():
    return pag.locateCenterOnScreen(f'{BUTTON_FOLDER}/ap.png')


def run_ship():
    pag.press('w', presses=5, interval=0.5)


while True:
    loc = in_port()
    if loc:
        print('In port.')
        select_ship()
        start_battle(loc)
    elif in_battle():
        print('In battle.')
        run_ship()
    elif is_battle_finish():
        print('Battle finished.')
        quit_battle()
    else:
        print('In else.')

    time.sleep(15)
