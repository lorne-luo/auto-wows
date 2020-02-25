import time
from random import randint

import pyautogui as pag

import settings as settings
from helper import search_template, get_map_image


class WOWS_Move(object):

    def move_ship(self):
        global MOVE_TO
        pag.press('m', presses=1, interval=0.25)
        pag.sleep(1.5)

        if not MOVE_TO:
            map_image = get_map_image()
            self_loc = search_template(map_image, 'map_self_icon.bmp')
            print('self_loc', self_loc)

            if self_loc:
                MOVE_TO = (settings.BATTLE_MAP_TOPLEFT[0] + settings.BATTLE_MAP_SIZE[0] - self_loc[1],
                           settings.BATTLE_MAP_TOPLEFT[1] + settings.BATTLE_MAP_SIZE[1] - self_loc[0])
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
