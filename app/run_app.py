import time

from app.core.actions.full_cycle_in_window import full_cycle_in_window
from app.core.actions.times.print_next_launch_time_pretty import print_next_launch_time_pretty
from app.core.constants import ALL_BS_WINDOWS, WIN_START, SETTINGS_FILE, ONE_DAY
from app.core.introduction.tesseract import setup_tesseract
from app.core.managers.time_checker import timer_checker


def run_app():
    setup_tesseract()

    while True:
        seconds_until_next_launch = print_next_launch_time_pretty(
            file_path=SETTINGS_FILE,
            num_windows=ALL_BS_WINDOWS,
            interval_seconds=ONE_DAY
        )

        time.sleep(seconds_until_next_launch + 1)

        for i in range(ALL_BS_WINDOWS):
            BS_WINDOW_NUMERIC = i
            BS_WINDOW_CORDS = WIN_START[f"win{i}"]["cords"]

            if timer_checker(
                    seconds=ONE_DAY,
                    window_number=BS_WINDOW_NUMERIC,
                    path_to_settings_file=SETTINGS_FILE,
            ):
                full_cycle_in_window(BS_WINDOW_NUMERIC=BS_WINDOW_NUMERIC, BS_WINDOW_CORDS=BS_WINDOW_CORDS)
