import time
import pathlib
import random
import logging
from datetime import datetime, timedelta
from typing import Final

import pyautogui as pg

from modules.config_manager import load_data, save_data
from modules.window_manager import (
    find_manager_window,
    stop_bs_windows,
    activate_main_window
)
from modules.image_finder import (
    delay,
    hunt_for_the_button_in_list,
    cycle_hunter_click,
    find_it_and_click_it
)


class PiFarm:
    def __init__(self, settings_file: str = "Settings.json"):
        """
        :param settings_file: Имя (или путь) к JSON-файлу с настройками, где хранятся таймеры.
        """
        self.settings_file = settings_file
        # Путь до JSON
        self.path_to_Settings: Final[pathlib.Path] = (
            pathlib.Path(__file__).parent.parent / settings_file
        )

        # Словарь с координатами для менеджера BlueStacks
        self.WIN_START = {
            "win0": {"cords": (540, 200)},
            "win1": {"cords": (540, 250)},
            "win2": {"cords": (540, 310)},
            "win3": {"cords": (540, 360)},
            "win4": {"cords": (540, 420)},
            "win5": {"cords": (540, 470), "MAIN_WINDOW": True},
        }
        self.window_numbers = len(self.WIN_START)

    def activate_window(self, win, win_numeric: int):
        """
        Активация окна в BlueStacks Multi Instance Manager (win),
        затем переносим его в (0,0), кликаем на нужную позицию,
        активируем основное окно эмулятора и делаем набор действий:
        - skip_option
        - connect_to_vpn_AND_open_telegram
        - Telegram
        - main_group
        """

        # Многократная активация и перемещение, чтобы окно точно стало сверху
        for _ in range(16):
            win.activate()
            win.move(0, 0)
            delay(0.01, 0.04)

        # Кликаем по координатам окна (например, выбрать нужную строку)
        pg.click(self.WIN_START[f"win{win_numeric}"]["cords"])
        delay(30, 40)

        # Активируем основное окно эмулятора
        activate_main_window()

        # Пропускать опции
        hunt_for_the_button_in_list(skip_option, hunt_in_seconds=2, threshold=0.88)

        # Кликаем цепочку: VPN, Telegram и т.п.
        cycle_hunter_click(connect_to_vpn_AND_open_telegram)
        delay()
        hunt_for_the_button_in_list(skip_option, hunt_in_seconds=2, threshold=0.88)
        find_it_and_click_it(Telegram, threshold=0.88)
        delay(20, 30)

        # Ищем кнопку/иконку групп main_group
        hunt_for_the_button_in_list(main_group, hunt_in_seconds=4)
        delay(14, 16)

    def start_farming(self, Game_Settings: dict):
        """
        Основной цикл.
        1) Ищет BlueStacks Multi Instance Manager
        2) Перебирает окна (win0..win5)
        3) Проверяет таймеры для каждой игры, если пора — активирует окно
        4) Запускает нужную функцию из Game_Settings
        5) Повтор каждые 3 минуты
        """
        while True:
            ACTIVATE = False
            manager_win = find_manager_window()
            if manager_win is None:
                logging.warning("BlueStacks Multi Instance Manager не найден. Ожидание...")
                time.sleep(30)
                continue

            for i in range(self.window_numbers):
                # Проверяем все игры, может ли хоть одна из них сработать
                for game, value in Game_Settings.items():
                    sec = value["seconds"]
                    if self.timer_checker(seconds=sec, window_number=i, game=game):
                        ACTIVATE = True

                # Если нашли игру, время которой пришло
                if ACTIVATE:
                    # Останавливаем все окна (закрываем) через Manager
                    stop_bs_windows()
                    # Активируем именно окно i
                    self.activate_window(manager_win, i)

                    # Для всех игр проверяем, кому пора
                    for game, value in Game_Settings.items():
                        sec = value["seconds"]
                        if self.timer_checker(seconds=sec, window_number=i, game=game):
                            # Вызываем функцию-обработчик (например, фарм)
                            # Передаём, является ли это "главным" окном (i == 5)
                            value["function"](win_main=(i == 0))

                            # Обновляем таймер
                            self.timer_update(window_numeric=i, game=game)

                    logging.info(
                        f"Текущее время: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}, Номер окна: {i}"
                    )
                    # Снова закрываем окна
                    stop_bs_windows()
                    # Сбрасываем флажок
                    ACTIVATE = False

            # Ждём 3 минуты перед повтором
            time.sleep(180)

    def timer_update(self, window_numeric: int, game: str):
        """
        Записывает в JSON текущее время как время последнего запуска для (window_numeric, game).
        """
        Settings = load_data(self.path_to_Settings)
        key_win = f"win{window_numeric}"
        if key_win not in Settings:
            Settings[key_win] = {}

        Settings[key_win][f"time_start_{game}"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(self.path_to_Settings, Settings)

    def timer_checker(self, seconds: int, window_number: int, game: str) -> bool:
        """
        Проверяет, прошло ли не менее 'seconds' секунд с момента
        последнего запуска game на окне window_number.
        """
        if not seconds:
            return False

        Settings = load_data(self.path_to_Settings)
        key_win = f"win{window_number}"
        time_key = f"time_start_{game}"
        default_timestamp = "2002-10-29 10:00:00"

        if key_win not in Settings:
            Settings[key_win] = {}

        if time_key not in Settings[key_win]:
            Settings[key_win][time_key] = default_timestamp
            save_data(self.path_to_Settings, Settings)

        try:
            last_timestamp = datetime.strptime(
                Settings[key_win][time_key], "%Y-%m-%d %H:%M:%S"
            )
        except (ValueError, KeyError, TypeError):
            Settings[key_win][time_key] = default_timestamp
            save_data(self.path_to_Settings, Settings)
            last_timestamp = datetime.strptime(default_timestamp, "%Y-%m-%d %H:%M:%S")

        current_time = datetime.now()
        return (current_time - last_timestamp) >= timedelta(seconds=seconds)

    @staticmethod
    def get_declension(number, forms):
        if 11 <= number % 100 <= 14:
            return forms[2]
        elif number % 10 == 1:
            return forms[0]
        elif 2 <= number % 10 <= 4:
            return forms[1]
        else:
            return forms[2]

    def time_end_print(self, time_end: float, time_start: float):
        """
        Красиво выводит общее время работы скрипта.
        """
        elapsed_time = time_end - time_start
        days = int(elapsed_time // (24 * 3600))
        hours = int((elapsed_time % (24 * 3600)) // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        day_form = self.get_declension(days, ["день", "дня", "дней"])
        hour_form = self.get_declension(hours, ["час", "часа", "часов"])
        minute_form = self.get_declension(minutes, ["минута", "минуты", "минут"])
        second_form = self.get_declension(seconds, ["секунда", "секунды", "секунд"])

        logging.info(
            f"Время работы процесса: {days} {day_form}, "
            f"{hours} {hour_form}, {minutes} {minute_form}, {seconds} {second_form}"
        )

    def Run_Pi(self, win_main: bool = False):
        """
        Пример функции "сбора наград" для Pi (заглушка).
        Можно дописать свою логику.
        """
        logging.info("Выполняется фарм Pi...")
        delay(2, 3)
        logging.info("Фарм Pi завершён.")
