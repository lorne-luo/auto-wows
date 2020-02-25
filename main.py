import time

import pyautogui as pag
from pyautogui._window_win import getWindow

import settings as settings
from wows.battle import WOWS_BATTLE
from wows.fire import WOWS_Fire
from wows.move import WOWS_Move
from wows.port import WOWS_PORT

pag.PAUSE = 0
pag.FAILSAFE = False


class WOWS(WOWS_PORT, WOWS_BATTLE, WOWS_Move, WOWS_Fire):
    FIRST_MOVED = False
    FIRE_ROUNDS = 0
    MOVE_TO = None

    SHIPS = [
        (138, 957),
        (138, 1024),
        # (138,1100),
    ]

    def focus_wows(self):
        wows_window = getWindow(settings.WINDOW_TITLE)
        wows_window.restore()
        wows_window.set_position(*settings.WINDOW_POSITION)
        wows_window.set_foreground()  # switch to wows window

    def quit_esc(self):
        if pag.pixelMatchesColor(*settings.QUIT_BATTLE_FINISHED_BUTTON2,
                                 settings.BUTTON_COLOR,
                                 tolerance=5):
            pag.press('esc')
            time.sleep(3)

        if pag.pixelMatchesColor(*settings.QUIT_BATTLE_FINISHED_BUTTON,
                                 settings.BUTTON_COLOR,
                                 tolerance=5):
            pag.press('esc')
            time.sleep(10)


if __name__ == '__main__':
    wows = WOWS()
    wows.focus_wows()
    wows.quit_esc()

    # switch to port
    pag.moveTo(settings.PORT_BUTTON, duration=0.25)
    pag.click(clicks=2, interval=1, button='left')

    while True:
        wows.focus_wows()

        if wows.in_battle():
            if wows.is_alive():
                if not wows.FIRST_MOVED:
                    print('In battle. alive')
                    wows.start_battle()
                wows.fire_ship()
            else:
                print('In battle. dead')
                wows.quit_battle()
                continue
        elif wows.in_port():
            wows.select_ship()
        else:
            # print('In else, sleep 5 secs')
            time.sleep(5)
        wows.quit_esc()
