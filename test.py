import os
import time

import pyautogui as pag

# pag.PAUSE = 1

BUTTON_FOLDER = 'buttons'
SHIP_FOLDER = 'ships'

ship1=(174,977)
start_button=(1182,62)
QUIT_BUTTON_LOC=(1177,514)


def quit_battle():
    quit_esc()
    loc = pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,'quit_battle_button.bmp'))
    if loc:
        # quit button already here

        pag.click(x=loc.x, y=loc.y, clicks=2, interval=1, button='left')
    else:
        quit_esc()
        pag.press('esc')
        pag.click(QUIT_BUTTON_LOC, clicks=2, interval=1, button='left')
def quit_esc():
    pics=['back_game.bmp','back_port.bmp','close.bmp']
    for pic in pics:
        loc = pag.locateCenterOnScreen(os.path.join(BUTTON_FOLDER,pic))
        if loc:
            pag.moveTo(loc)
            pag.click(loc,clicks=2, interval=1, button='left')
            # pag.press('esc')
            time.sleep(4)

pag.click(70,14)

quit_battle()
# pag.press('esc')
# pag.click(QUIT_BUTTON_LOC, clicks=2, interval=1, button='left')


# while True:
#     t3=os.path.join(BUTTON_FOLDER,'esc.bmp')
#     print(pag.locateCenterOnScreen(t3))
#
# # window=os.path.join(BUTTON_FOLDER,'wows_window.png')
# test=os.path.join(BUTTON_FOLDER,'test.bmp')


# pag.moveTo(ship1)
# pag.click(ship1,clicks=2, interval=1, button='left')
#
#
# pag.moveTo(start_button)
# pag.click(start_button,clicks=2, interval=1, button='left')

# while True:
    # print(pag.locateCenterOnScreen(test))

# point=(2332,1168)
# pix=pag.pixel(*point)
# print(pix in [(14,31,35),(3, 45, 33)])
