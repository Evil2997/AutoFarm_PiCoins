import json
import pathlib
import random
import time
from datetime import datetime, timedelta
from typing import Final

import cv2
import numpy as np
import pyautogui as pg
from PIL import ImageGrab
from ahk import AHK

from modules.tesseract import setup_tesseract

ahk = AHK()


class PiFarm:
    def __init__(self):
        self.WIN_START = {
            "win0": {"cords": (540, 200)},
            "win1": {"cords": (540, 250)},
            "win2": {"cords": (540, 310)},
            "win3": {"cords": (540, 360)},
            "win4": {"cords": (540, 420)},
            "win5": {"cords": (540, 470), "MAIN_WINDOW": True},
        }
        self.window_numbers = len(self.WIN_START)

    def start_farming(self, window_numbers, settings_file):
        while True:
            ACTIVATE = False
            for win in ahk.list_windows():
                if win.title.startswith("BlueStacks Multi Instance Manager"):
                    for i in range(window_numbers):
                        win_main = (i == 5)
                        for game, value in Game_Settings.items():
                            sec = value["seconds"]
                            if self.timer_checker(seconds=sec, window_number=i, game=game, settings_file=settings_file):
                                ACTIVATE = True
                        if ACTIVATE:
                            self.Stop_BS_Windows()
                            self.activate_window(win, i)
                            for game, value in Game_Settings.items():
                                sec = value["seconds"]
                                if self.timer_checker(seconds=sec, window_number=i, game=game, settings_file=settings_file):
                                    Game_Settings[game]["function"](
                                        win_main=win_main)
                                    self.timer_update(
                                        window_numeric=i,
                                        game=game,
                                        settings_file=settings_file
                                    )
                            print(
                                f"Текущее время: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}, Номер окна: {i}"
                            )

                            self.Stop_BS_Windows()
                            ACTIVATE = False
                    time.sleep(180)
                    break

    def timer_update(self, settings_file, window_numeric, game):
        i = window_numeric
        path_to_Settings: Final[pathlib.Path] = pathlib.Path(__file__).parent.parent / settings_file
        Settings = self.load_data(path_to_Settings)

        Settings[f"win{i}"][f"time_start_{game}"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_data(path_to_Settings, Settings)


    def save_data(self, file_path, data):
        with open(file_path, 'w') as jf:
            json.dump(data, jf, indent=2)


    def timer_checker(self, seconds, window_number, game, settings_file):
        if seconds:
            i = window_number
            path_to_Settings: Final[pathlib.Path] = pathlib.Path(__file__).parent.parent / settings_file
            Settings = self.load_data(path_to_Settings)

            default_timestamp_HUMAN = "2002-10-29 10:00:00"
            current_time = datetime.now()

            win_key = f"win{i}"
            time_key = f"time_start_{game}"

            if win_key not in Settings:
                Settings[win_key] = {}

            if time_key not in Settings[win_key]:
                Settings[win_key][time_key] = default_timestamp_HUMAN
                self.save_data(path_to_Settings, Settings)

            try:
                timestamp = datetime.strptime(Settings[win_key][time_key], "%Y-%m-%d %H:%M:%S")
            except (ValueError, KeyError, TypeError):
                Settings[win_key][time_key] = default_timestamp_HUMAN
                self.save_data(path_to_Settings, Settings)
                timestamp = datetime.strptime(default_timestamp_HUMAN, "%Y-%m-%d %H:%M:%S")

            time_difference = current_time - timestamp
            if time_difference >= timedelta(seconds=seconds):
                return True
        return False


    def time_end_print(self, time_end, time_start):
        def get_declension(number, forms):
            if 11 <= number % 100 <= 14:
                return forms[2]
            elif number % 10 == 1:
                return forms[0]
            elif 2 <= number % 10 <= 4:
                return forms[1]
            else:
                return forms[2]

        elapsed_time = time_end - time_start
        days = elapsed_time // (24 * 3600)
        hours = (elapsed_time % (24 * 3600)) // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = elapsed_time % 60

        day_form = get_declension(int(days), ["день", "дня", "дней"])
        hour_form = get_declension(int(hours), ["час", "часа", "часов"])
        minute_form = get_declension(int(minutes), ["минута", "минуты", "минут"])
        second_form = get_declension(int(seconds), ["секунда", "секунды", "секунд"])

        print(
            f"Время работы процесса: {int(days)} {day_form}, {int(hours)} {hour_form}, {int(minutes)} {minute_form}, {int(seconds)} {second_form}")



    def hunt_for_the_button_in_list(self, name_list: list[str], hunt_in_seconds=10, region=(0, 0, 1920, 1080), threshold=0.92):
        for name in name_list:
            time_start = time.time()
            while time.time() - time_start < hunt_in_seconds:
                top_left = self.find_template_in_region(name, region, threshold=threshold)
                width, height = self.get_image_size(name)
                if top_left:
                    self.delay(0.2, 0.3)
                    pg.click(top_left[0] + width / 2, top_left[1] + height / 2)
                    return True
                else:
                    self.delay(0.01, 0.1)
        return False


    def get_image_size(self, image_name):
        image_path = f"Images/{image_name}.png"
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found: {image_path}")
        height, width, _ = image.shape
        return width, height


    def find_template_in_region(
            self,
            template_name: str,
            region: tuple[int, int, int, int] = (0, 0, 1920, 1080),
            threshold: float = 0.92,
            template_path: str = "Images/"
    ) -> tuple[int, int] | None:
        template_full_path = f"{template_path}{template_name}.png"

        (x1, y1, x2, y2) = region
        screenshot = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))  # Захватываем регион экрана
        template = cv2.imread(template_full_path, cv2.IMREAD_GRAYSCALE)

        if template is None:
            raise FileNotFoundError(f"Template image not found: {template_full_path}")

        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)  # Преобразуем скриншот в grayscale

        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            top_left = (max_loc[0] + region[0], max_loc[1] + region[1])  # Корректируем координаты для всей области экрана
            return top_left

        return None


    def cycle_hunter_click(self, name_list: list[str], region=(0, 0, 1920, 1080)):
        for name in name_list:
            while True:
                top_left = self.find_template_in_region(name, region)
                width, height = self.get_image_size(name)
                if top_left:
                    self.delay(0.2, 0.3)
                    pg.click(top_left[0] + width / 2, top_left[1] + height / 2)
                    break
                else:
                    self.delay(0.04, 0.2)
            self.delay(0.8, 1.2)


    def find_it_and_click_it(self, name_list: list[str], region=(0, 0, 1920, 1080), threshold=0.92):
        for name in name_list:
            top_left = self.find_template_in_region(name, region, threshold=threshold)
            width, height = self.get_image_size(name)
            if top_left:
                self.delay(0.2, 0.3)
                pg.click(top_left[0] + width / 2, top_left[1] + height / 2)
                if len(name_list) == 1:
                    return True
            elif len(name_list) == 1:
                return False




    def load_data(self, file_path):
        with open(file_path, 'r') as jf:
            return json.load(jf)


    def Run_Pi(self):
        # алгоритм сбора необходимых наград.
        pass


    def delay(self, min_seconds: float = 1.0, max_seconds: float = 2.0):
        time.sleep(random.uniform(min_seconds, max_seconds))


    def Stop_BS_Windows(self ):
        close_all_BS_window = [(350, 590), (500, 360)]

        for win in ahk.list_windows():
            if win.title.startswith("BlueStacks Multi Instance Manager"):
                for _ in range(8):
                    win.activate()
                    self.delay(0.02, 0.2)
                for coordinates in close_all_BS_window:
                    pg.click(coordinates)
                    self.delay(1.6, 3.2)


if __name__ == '__main__':
    setup_tesseract()

    MAIN_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent

    settings_file = "Settings.json"
    path_to_Settings: Final[pathlib.Path] = MAIN_DIR / settings_file
    Settings = load_data(path_to_Settings)

    SS = Seconds_time_to_Started = random.randint(30, 40)

    Game_Settings = {
        "Pi": {"seconds": 24 * 3600 - SS, "function": Run_Pi},
    }

    # [RUN_SCRIPT]---[START]
    time_start = time.time()
    try:
        main()
    except KeyboardInterrupt:
        pass
    print(f"Время окончания сеанса: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    time_end = time.time()
    time_end_print(time_end, time_start)
    # [RUN_SCRIPT]---[END]
