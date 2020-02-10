import pyautogui as pag

pag.PAUSE = 0
pag.FAILSAFE = False
from helper import *

BUTTON_FOLDER = 'buttons'
SHIP_FOLDER = 'ships'

ship1 = (174, 977)
start_button = (1182, 62)
QUIT_BUTTON_LOC = (1177, 514)

if __name__ == '__main__':
    r = pag.pixelMatchesColor(*(1712, 33), (39, 40, 34), tolerance=10)
    print(r)
