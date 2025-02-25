import pathlib
import time
from datetime import datetime, timedelta
from typing import Final

import pyautogui as pg

from core.config import load_data, save_data
from utils.constants import (
    ACTIVATION_ITERATIONS,
    ACTIVATION_MOVE_DELAY_MIN,
    ACTIVATION_MOVE_DELAY_MAX,
    WAIT_AFTER_CLICK_MIN,
    WAIT_AFTER_CLICK_MAX,
    SLEEP_IF_NO_MANAGER,
    SLEEP_BETWEEN_CYCLES,
    DEFAULT_TIMESTAMP,
    skip_option,
    connect_to_vpn_AND_open_telegram,
    Telegram,
    main_group,
    DEFAULT_DELAY_MIN,
    DEFAULT_DELAY_MAX,
    WIN_START,
)
from utils.logger import logger
from managers.window import find_manager_window, stop_bs_windows, activate_this_bs_window
from utils.unified_hunt_click import delay, unified_hunt_click
from utils.time_formatter import format_elapsed_time


class PiFarm:
    def __init__(self, settings_file: str = "Settings.json"):
        self.settings_file = settings_file
        self.path_to_Settings: Final[pathlib.Path] = pathlib.Path(__file__).parent.parent / settings_file
        self.window_numbers = len(WIN_START)

    def activate_window(self, win, win_numeric: int):
        for _ in range(ACTIVATION_ITERATIONS):
            win.activate()
            win.move(0, 0)
            delay(ACTIVATION_MOVE_DELAY_MIN, ACTIVATION_MOVE_DELAY_MAX)
        pg.click(WIN_START[f"win{win_numeric}"]["cords"])
        delay(WAIT_AFTER_CLICK_MIN, WAIT_AFTER_CLICK_MAX)
        unified_hunt_click([skip_option], mode="hunt", timeout=2, threshold=0.88)
        unified_hunt_click([connect_to_vpn_AND_open_telegram], mode="cycle")
        delay(DEFAULT_DELAY_MIN, DEFAULT_DELAY_MAX)
        unified_hunt_click([skip_option], mode="hunt", timeout=2, threshold=0.88)
        unified_hunt_click([Telegram], mode="once", threshold=0.88)
        delay(20, 30)
        unified_hunt_click([main_group], mode="hunt", timeout=4)
        delay(14, 16)

    def start_farming(self, Game_Settings: dict):
        while True:
            ACTIVATE = False
            manager_win = find_manager_window()
            if manager_win is None:
                logger.warning("BlueStacks Multi Instance Manager не найден. Ожидание...")
                time.sleep(SLEEP_IF_NO_MANAGER)
                continue
            for i in range(self.window_numbers):
                for game, value in Game_Settings.items():
                    sec = value["seconds"]
                    if self.timer_checker(seconds=sec, window_number=i, game=game):
                        ACTIVATE = True
                if ACTIVATE:
                    stop_bs_windows()
                    self.activate_window(manager_win, i)
                    for game, value in Game_Settings.items():
                        sec = value["seconds"]
                        if self.timer_checker(seconds=sec, window_number=i, game=game):
                            value["function"](win_main=(i == 0))
                            self.timer_update(window_numeric=i, game=game)
                    logger.info(
                        f"Текущее время: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}, Номер окна: {i}")
                    stop_bs_windows()
                    ACTIVATE = False
            time.sleep(SLEEP_BETWEEN_CYCLES)

    def timer_update(self, window_numeric: int, game: str):
        Settings = load_data(self.path_to_Settings)
        key_win = f"win{window_numeric}"
        if key_win not in Settings:
            Settings[key_win] = {}
        Settings[key_win][f"time_start_{game}"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(self.path_to_Settings, Settings)

    def timer_checker(self, seconds: int, window_number: int, game: str) -> bool:
        if not seconds:
            return False
        Settings = load_data(self.path_to_Settings)
        key_win = f"win{window_number}"
        time_key = f"time_start_{game}"
        if key_win not in Settings:
            Settings[key_win] = {}
        if time_key not in Settings[key_win]:
            Settings[key_win][time_key] = DEFAULT_TIMESTAMP
            save_data(self.path_to_Settings, Settings)
        try:
            last_timestamp = datetime.strptime(Settings[key_win][time_key], "%Y-%m-%d %H:%M:%S")
        except (ValueError, KeyError, TypeError):
            Settings[key_win][time_key] = DEFAULT_TIMESTAMP
            save_data(self.path_to_Settings, Settings)
            last_timestamp = datetime.strptime(DEFAULT_TIMESTAMP, "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - last_timestamp) >= timedelta(seconds=seconds)

    def print_time_end(self, time_end: float, time_start: float):
        logger.info(format_elapsed_time(time_end, time_start))

    def Run_Pi(self, win_main: bool = False):
        logger.info("Выполняется фарм Pi...")
        delay(2, 3)
        logger.info("Фарм Pi завершён.")
