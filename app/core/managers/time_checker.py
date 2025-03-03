import pathlib
from datetime import datetime, timedelta
from typing import Final

from app.core.constants import default_timestamp_HUMAN, time_key
from app.core.managers.config import load_data, save_data


def timer_checker(seconds, window_number, path_to_settings_file):
    if seconds:
        i = window_number
        Settings = load_data(path_to_settings_file)

        current_time = datetime.now()

        win_key = f"win{i}"

        if win_key not in Settings:
            Settings[win_key] = {}

        if time_key not in Settings[win_key]:
            Settings[win_key][time_key] = default_timestamp_HUMAN
            save_data(path_to_settings_file, Settings)

        try:
            timestamp = datetime.strptime(Settings[win_key][time_key], "%Y-%m-%d %H:%M:%S")
        except (ValueError, KeyError, TypeError):
            Settings[win_key][time_key] = default_timestamp_HUMAN
            save_data(path_to_settings_file, Settings)
            timestamp = datetime.strptime(default_timestamp_HUMAN, "%Y-%m-%d %H:%M:%S")

        time_difference = current_time - timestamp
        if time_difference >= timedelta(seconds=seconds):
            return True
    return False


def timer_update(path_to_settings_file, window_numeric):
    i = window_numeric
    Settings = load_data(path_to_settings_file)

    Settings[f"win{i}"][time_key] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_data(path_to_settings_file, Settings)
