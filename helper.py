import os

import pyautogui as pag

import settings as settings


def check_pic(filename):
    return pag.locateCenterOnScreen(os.path.join(settings.BUTTON_FOLDER, f'{filename}.bmp'))
