import os
from math import sqrt

import cv2
import numpy as np
import pyautogui as pag

import settings as settings


def check_pic(filename):
    return pag.locateCenterOnScreen(os.path.join(settings.BUTTON_FOLDER, f'{filename}.bmp'))


def get_battle_field_image():
    topleft = settings.BATTLE_FIELD_TOPLEFT
    bottomright = settings.BATTLE_FIELD_BOTTOMRIGHT
    battle_field_image = pag.screenshot(region=(topleft[0], topleft[1],
                                                bottomright[0] - topleft[0], bottomright[1] - topleft[1]))
    battle_field_image = cv2.cvtColor(np.array(battle_field_image), cv2.COLOR_RGB2BGR)
    return battle_field_image


def search_enemy_ships(image, ship_type):
    ship_icon = cv2.imread(f'buttons/{ship_type}.png')
    width, height = ship_icon.shape[:2]
    result = cv2.matchTemplate(ship_icon, image, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(result >= threshold)
    return [(pt[0] + width / 2, pt[1] + height / 2) for pt in zip(*loc[::-1])]  # Switch collumns and rows


def distance(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    return sqrt(x ** 2 + y ** 2)


def select_nearest_enemy(locs):
    nearest_loc = None
    nearest_distance = 2560 ** 2
    for loc in locs:
        dis = distance(settings.AIMING_CENTER, loc)
        if dis < nearest_distance:
            nearest_loc = loc
            nearest_distance = dis
    return nearest_loc
