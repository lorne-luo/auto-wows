import ctypes
import settings
from pyautogui._window_win import getWindow
import pyautogui as pag

MOUSEEVENT_MOVE = 0x0001
FACTOR = 1.2
LOOP = 10


def move_mouse(x, y):
    pag.sleep(1)
    x = int(x / LOOP / FACTOR)
    y = int(y / LOOP / FACTOR)

    for i in range(10):
        ctypes.windll.user32.mouse_event(MOUSEEVENT_MOVE, x, y, 0, 0)
        pag.sleep(0.01)


if __name__ == '__main__':
    wows_window = getWindow(settings.WINDOW_TITLE)
    wows_window.set_foreground()  # switch to wows window

    # move_ship()
    # fire_ship()
    # move_mouse(400, 0)
    y = -50
    x = 500
    move_mouse(x, y)
