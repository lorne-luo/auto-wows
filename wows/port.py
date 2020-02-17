import sys
import time

import pyautogui as pag

import settings as settings

pag.PAUSE = 0
pag.FAILSAFE = False

FIRST_MOVED = False
FIRE_ROUNDS = 0
MOVE_TO = None

SHIPS = [
    (174, 967),
    (174, 1030),
    # (174,1100),
]


class WOWS_PORT(object):

    def check_battle_mode(self):
        if not pag.pixelMatchesColor(*settings.BATTLE_MODE,
                                     (14, 80, 79),
                                     tolerance=10):
            print('Please check battle mode.')
            sys.exit(0)

    def in_port(self):
        point = settings.SHIP_FILTER_BUTTON
        color = (148, 198, 199)
        result = pag.pixelMatchesColor(*point, color, tolerance=10)
        if result:
            print('In port.')

        return result

    def select_ship(self):
        for loc in SHIPS:
            # print(f'Ship select {loc}')
            pag.moveTo(loc, duration=0.25)
            pag.click(clicks=3, interval=1, button='left')
            time.sleep(2)

            # print(f'Enter battle')
            pag.moveTo(settings.START_BUTTON, duration=0.25)
            pag.click(clicks=3, interval=0.5, button='left')

            if not self.in_port():
                break

        self.FIRST_MOVED = False
