import time

from app.core.actions.full_cycle_in_window import full_cycle_in_window
from app.core.checker.time_until_next_launch import time_until_next_launch
from app.core.constants import ALL_BS_WINDOWS, WIN_START, SETTINGS_FILE, ONE_DAY
from app.core.introduction.tesseract import setup_tesseract
from app.core.managers.time_checker import timer_checker
from app.logs.logger import logger


def run_app():
    setup_tesseract()

    while True:
        seconds_until_next = time_until_next_launch(SETTINGS_FILE, ALL_BS_WINDOWS)
        for i in range(ALL_BS_WINDOWS):
            BS_WINDOW_NUMERIC = i
            BS_WINDOW_CORDS = WIN_START[f"win{i}"]["cords"]

            if timer_checker(
                    seconds=ONE_DAY,
                    window_number=BS_WINDOW_NUMERIC,
                    path_to_settings_file=SETTINGS_FILE,
            ):
                full_cycle_in_window(BS_WINDOW_NUMERIC=BS_WINDOW_NUMERIC, BS_WINDOW_CORDS=BS_WINDOW_CORDS)
        logger.info(f"Цикл завершён. Следующий запуск через {seconds_until_next} секунд.")
        time.sleep(seconds_until_next)
