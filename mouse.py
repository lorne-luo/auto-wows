import time

import ctypes
from pyautogui._window_win import getWindow
import pyautogui as pag
from wows import *


MOUSEEVENT_MOVE = 0x0001
FACTOR = 1.3
LOOP = 10

def move_mouse(x, y):
    time.sleep(1)
    x = x/LOOP/FACTOR
    y = y/LOOP/FACTOR

    for i in range(10):
        ctypes.windll.user32.move_mouse(x, y, 0, 0)
        time.sleep(0.01)

if __name__ == '__main__':
    wows_window = getWindow('World of Warships')
    wows_window.set_foreground()  # switch to wows window

    # move_ship()
    # fire_ship()
    # move_mouse(400, 0)
    y = -50
    x = 500
    move_mouse(x, y)
