import json
from datetime import datetime, timedelta

from app.core.constants import SETTINGS_FILE, ALL_BS_WINDOWS, ONE_DAY


def time_until_next_launch(
        file_path: str = SETTINGS_FILE,
        num_windows: int = ALL_BS_WINDOWS,
        interval_seconds: int = ONE_DAY,
) -> int:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Сортировка окон по порядковому номеру (win0, win1, ...)
    windows = sorted(
        ((key, value) for key, value in data.items() if key.startswith("win")),
        key=lambda x: int(x[0].replace("win", ""))
    )
    windows = windows[:num_windows]

    now = datetime.now()
    next_launch_times = []

    for key, window in windows:
        time_start_str = window.get("time_start")
        try:
            last_launch = datetime.strptime(time_start_str, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"Ошибка разбора времени для {key}: {time_start_str}")
            continue

        next_launch = last_launch + timedelta(seconds=interval_seconds)
        diff_seconds = (next_launch - now).total_seconds()
        next_launch_times.append(max(0, diff_seconds))

    if not next_launch_times:
        return 0

    return int(min(next_launch_times))
