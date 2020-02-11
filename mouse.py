import time

from ctypes.windll.user32 import mouse_event

MOUSEEVENT_MOVE = 0x0001


def move_mouse(x, y):
    mouse_event(MOUSEEVENT_MOVE, x, y, 0, 0)


if __name__ == '__main__':
    for i in range(100):
        move_mouse(1, 1)
        time.sleep(0.01)
