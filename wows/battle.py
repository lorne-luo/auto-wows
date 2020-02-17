import time

import pyautogui as pag

import settings as settings


class WOWS_BATTLE(object):
    FIRST_MOVED = False
    FIRE_ROUNDS = 1
    MOVE_TO = None

    def in_battle(self):
        return pag.pixelMatchesColor(*settings.SHIP_TYPE_ICON,
                                     settings.BUTTON_COLOR,
                                     tolerance=5)

    def quit_battle(self):
        pag.press('esc')
        time.sleep(2)
        # print('quit_battle.click')
        pag.moveTo(settings.QUIT_BATTLE_BUTTON, duration=0.25)
        pag.click(clicks=2, interval=0.5, button='left')
        time.sleep(1)

        pag.moveTo(settings.QUIT_BATTLE_CONFIRM_BUTTON, duration=0.25)
        pag.click(clicks=2, interval=0.5, button='left')
        time.sleep(11)
        global FIRST_MOVED
        FIRST_MOVED = False

    def is_alive(self):
        result = sum([pag.pixelMatchesColor(*settings.SPEED_S, settings.BATTLE_SWM_COLOR, tolerance=50),
                      pag.pixelMatchesColor(*settings.SPEED_W, settings.BATTLE_SWM_COLOR, tolerance=50),
                      pag.pixelMatchesColor(*settings.SPEED_M, settings.BATTLE_SWM_COLOR, tolerance=50)]) > 1
        return result

    def start_battle(self):
        self.MOVE_TO = None
        pag.press('w', presses=5, interval=0.25)
        pag.press('1')
        pag.press('y', presses=2, interval=0.25)
        pag.press('u', presses=2, interval=0.25)
        pag.sleep(1)

        self.move_ship()

        self.FIRST_MOVED = True
        self.FIRE_ROUNDS = 1
        pag.sleep(20)
