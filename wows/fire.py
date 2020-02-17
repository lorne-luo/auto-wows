import cv2
import numpy as np
import pyautogui as pag

import settings as settings
from helper import get_battle_field_image, distance
from mouse import move_mouse


class WOWS_Fire(object):
    ENEMY_OFFSET = (35, 39)
    FIREB_LOCKED = (1299, 607)

    def list_enemy(self, image):
        ship_icon = cv2.imread(f'buttons/battle_blood.bmp')
        width, height = ship_icon.shape[:2]
        result = cv2.matchTemplate(ship_icon, image, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(max_val, max_loc)

        threshold = .86
        loc = np.where(result >= threshold)
        # print(loc)

        return [(pt[0] + self.ENEMY_OFFSET[0],
                 pt[1] + self.ENEMY_OFFSET[1]) for pt in zip(*loc[::-1]) if
                pt[0] < settings.BATTLE_MINIMAP_TOPLEFT[0] and
                pt[1] < settings.BATTLE_MINIMAP_TOPLEFT[1]]

    def select_enemy(self):
        battle_field_image = get_battle_field_image()
        enemy_locs = self.list_enemy(battle_field_image)

        enemy_dict = {}
        for loc in enemy_locs:
            dis = distance(settings.CROSSHAIR, loc)
            enemy_dict[dis] = loc

        return enemy_dict

    #
    # def select_nearest_enemy(self, locs):
    #     nearest_loc = None
    #     nearest_distance = 2560 ** 2
    #     for loc in locs:
    #         dis = distance(settings.CROSSHAIR, loc)
    #         if dis < nearest_distance:
    #             nearest_loc = loc
    #             nearest_distance = dis
    #     return nearest_loc

    def move_crosshair(self, loc):
        AIMING_OFFSET = (0, 60)
        x = loc[0] - settings.CROSSHAIR[0]
        y = (AIMING_OFFSET[1] + loc[1]) - settings.CROSSHAIR[1]

        print(settings.CROSSHAIR, '->', loc)
        print(x, y)
        move_mouse(x, y)

    def fire_ship(self):
        # if not pag.pixelMatchesColor(*settings.AUTO_PILOT,
        #                              (76, 232, 170),
        #                              tolerance=30):
        #     self.move_ship()

        pag.press('`', presses=1, interval=0.25)
        pag.press('r', presses=1, interval=0.25)

        enemy_locs = self.select_enemy()
        # print(nearest_enemy_loc)

        if not enemy_locs:
            pag.sleep(5)
            return

        for dis in sorted(enemy_locs.keys()):
            loc = enemy_locs[dis]
            if self.try_fire(loc):
                break

        if not self.FIRE_ROUNDS % 10:
            # print(f'#{FIRE_ROUNDS} use consuption')
            pag.press('t', presses=1, interval=0.25)
            pag.press('y', presses=1, interval=0.25)
            pag.press('u', presses=1, interval=0.25)

        pag.sleep(1)
        self.FIRE_ROUNDS += 1

    def try_fire(self, loc):
        self.move_crosshair(loc)
        pag.sleep(2)

        if pag.pixelMatchesColor(self.FIREB_LOCKED,
                                 settings.BUTTON_COLOR,
                                 tolerance=30):
            return False

        for i in range(5):
            pag.press('r', presses=1, interval=0.25)
            if self.is_gun_ready():
                pag.click(clicks=2, interval=0.25)
                return True
            pag.sleep(2)

        return False

    def is_gun_ready(self):
        result = pag.pixelMatchesColor(*settings.GUN_READY,
                                       (30, 200, 120),
                                       tolerance=30)
        if not result:
            print('gun is not ready.')
        return result
