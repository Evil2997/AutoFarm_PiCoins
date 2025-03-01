import pathlib
from typing import Final

DEFAULT_REGION = (0, 0, 1920, 1080)
DEFAULT_THRESHOLD = 0.92
DEFAULT_HUNT_TIMEOUT = 10.0

CYCLE_INTERVAL = 24 * 60 * 60  # 24 часа

MANAGER_ACTIVATION_ATTEMPTS = 8

# Задержки для активации окна Manager (нижняя и верхняя границы)
MANAGER_ACTIVATION_DELAY_SHORT = 0.02
MANAGER_ACTIVATION_DELAY_UPPER = 0.2

# Задержки для кликов при закрытии окон BS
STOP_WINDOW_CLICK_DELAY = 1.6
STOP_WINDOW_CLICK_INTERVAL = 3.2

# Задержка по умолчанию для вызова функции delay() (нижняя и верхняя границы)
DEFAULT_DELAY_MIN = 1.0
DEFAULT_DELAY_MAX = 2.0

ACTIVATION_ITERATIONS = 16
ACTIVATION_MOVE_DELAY_MIN = 0.01
ACTIVATION_MOVE_DELAY_MAX = 0.04
WAIT_AFTER_CLICK_MIN = 30
WAIT_AFTER_CLICK_MAX = 40

SLEEP_IF_NO_MANAGER = 30
SLEEP_BETWEEN_CYCLES = 180

DEFAULT_TIMESTAMP = "2002-10-29 10:00:00"
# ======================================================================================================================
WIN_START = {
    "win0": {"cords": (540, 200)},
    "win1": {"cords": (540, 250)},
    "win2": {"cords": (540, 310)},
    "win3": {"cords": (540, 360)},
    "win4": {"cords": (540, 420)},
    "win5": {"cords": (540, 470)},
}

ALL_BS_WINDOWS = len(WIN_START)

MAIN_PROJECT_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parents[1]

IMAGE_PATHS: pathlib.Path = MAIN_PROJECT_DIR / pathlib.Path("Images")

full_screen = ["full_screen"]

PROTON_VPN = ["proton_vpn_open", "continue_without_registration", "vpn_plus__not_now", "proton_vpn_enable", "collapse_all_windows"]

APP_INSTALL = {
    "open_play_market": ["open_play_market"],
    "play_market_first_click": (980, 170),
    "open_loop_searcher_apps": (150, 530),
    "write_text_here": (500, 130),
    "TEXT_TO_WRITE_1": "Pi Network",
    "install_button": ["install_button"],
    "TEXT_TO_WRITE_2": "Pi Browser",
    "collapse_all_windows": ["collapse_all_windows"],
    "WAIT": 90,
}

FIRST_OPEN_APP = {
    "app_open": ["app_open_pi_network"],
    "continue_with_phone_number": ["continue_with_phone_number"],
    "click_to_write_text_1": (760, 550),
    "write_here_country_phone_number": "+380",
    "select_Ukraine": (840, 600),
    "click_to_write_text_2": (760, 640),
    "phone_number": "",
    "button_send": ["button_send"],
}

APP_OPEN_ICON = ["app_open_pi_network", "button_open_farming", "button_start_farming"]
BUTTON_CLOSE_BS_WINDOW = ["button_close_bs_window", "button_close_bs_window__yes"]

SETTINGS_FILE = pathlib.Path("Settings.json")
