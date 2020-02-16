import os
from math import sqrt

import cv2
import os
import numpy as np
import pyautogui as pag

import settings as settings


def check_pic(filename):
    return pag.locateCenterOnScreen(os.path.join(settings.BUTTON_FOLDER, f'{filename}.bmp'))


def get_battle_field_image():
    battle_field_image = pag.screenshot(region=(0, 0, settings.WINDOW_POSITION[2], settings.WINDOW_POSITION[3]))
    battle_field_image = cv2.cvtColor(np.array(battle_field_image), cv2.COLOR_RGB2BGR)
    return battle_field_image


def get_minimap_image():
    minimap_image = pag.screenshot(region=(settings.BATTLE_MINIMAP_TOPLEFT[0], settings.BATTLE_MINIMAP_TOPLEFT[1] + 150,
                                           settings.BATTLE_MINIMAP_SIZE[0], settings.BATTLE_MINIMAP_SIZE[0]))
    # minimap_image.save('minimap.bmp')
    minimap_image = cv2.cvtColor(np.array(minimap_image), cv2.COLOR_RGB2BGR)
    return minimap_image


def get_map_image():
    map_image = pag.screenshot(region=(settings.BATTLE_MAP_TOPLEFT[0], settings.BATTLE_MAP_TOPLEFT[1],
                                       settings.BATTLE_MAP_SIZE[0], settings.BATTLE_MAP_SIZE[1]))
    # map_image.save('map.bmp')
    map_image = cv2.cvtColor(np.array(map_image), cv2.COLOR_RGB2BGR)
    return map_image


def search_teamplate(image, template_file, return_all=False):
    template = cv2.imread(f'buttons/{template_file}')
    width, height = template.shape[:2]
    result = cv2.matchTemplate(template, image, cv2.TM_CCOEFF_NORMED)

    threshold = .85
    if not return_all:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > threshold:
            return (int(max_loc[0] + width / 2),
                    int(max_loc[1] + height / 2))
        else:
            return None

    loc = np.where(result >= threshold)
    all_matches = [(int(pt[0] + width / 2),
                    int(pt[1] + height / 2)) for pt in zip(*loc[::-1])]
    return all_matches


def search_enemy_ships(image, ship_type):
    ship_icon = cv2.imread(f'buttons/{ship_type}.bmp')
    width, height = ship_icon.shape[:2]
    result = cv2.matchTemplate(ship_icon, image, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(result >= threshold)
    # print(loc)

    return [(int(pt[0] + width / 2),
             int(pt[1] + height / 2)) for pt in zip(*loc[::-1]) if
            pt[0] < settings.BATTLE_MINIMAP_TOPLEFT[0] and
            pt[1] < settings.BATTLE_MINIMAP_TOPLEFT[1]]


def distance(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    return sqrt(x ** 2 + y ** 2)


def select_nearest_enemy(locs):
    nearest_loc = None
    nearest_distance = 2560 ** 2
    for loc in locs:
        dis = distance(settings.CROSSHAIR, loc)
        if dis < nearest_distance:
            nearest_loc = loc
            nearest_distance = dis
    return nearest_loc


def shutdown():
    pag.moveTo(settings.WINDOWS_START, duration=0.25)
    pag.click()

    pag.moveTo(settings.WINDOWS_START2, duration=0.25)
    pag.click()

    pag.moveTo(settings.WINDOWS_START3, duration=0.25)
    pag.click(clicks=2, interval=0.25)
