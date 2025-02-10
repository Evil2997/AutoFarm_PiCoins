import pathlib
import time
import random
from typing import Final

from modules.config_manager import load_data
from modules.tesseract import setup_tesseract
from modules.pi_farm import PiFarm

if __name__ == '__main__':
    setup_tesseract()

    MAIN_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent
    settings_file = "Settings.json"
    path_to_Settings: Final[pathlib.Path] = MAIN_DIR / settings_file
    _ = load_data(path_to_Settings)  # Если настройки нужны для внутренней логики PiFarm

    SS = random.randint(30, 40)

    pi_farm = PiFarm(settings_file=settings_file)

    Game_Settings = {
        "Pi": {"seconds": 24 * 3600 - SS, "function": pi_farm.Run_Pi},
    }

    time_start = time.time()
    try:
        pi_farm.start_farming(Game_Settings)
    except KeyboardInterrupt:
        pass
    print(f"Время окончания сеанса: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    time_end = time.time()
    pi_farm.print_time_end(time_end, time_start)
