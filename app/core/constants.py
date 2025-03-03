import pathlib
from typing import Final

MAIN_PROJECT_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parents[1]

IMAGE_PATHS: pathlib.Path = MAIN_PROJECT_DIR / pathlib.Path("Images")
SETTINGS_FILE = pathlib.Path = MAIN_PROJECT_DIR / pathlib.Path("Settings.json")


# ======================================================================================================================
DEFAULT_REGION = (0, 0, 1920, 1080)
DEFAULT_THRESHOLD = 0.92
ONE_DAY = 24 * 3600 - 34

WIN_START = {
    "win0": {"cords": (540, 200)},
    "win1": {"cords": (540, 250)},
    # "win2": {"cords": (540, 310)},
    # "win3": {"cords": (540, 360)},
    # "win4": {"cords": (540, 420)},
    # "win5": {"cords": (540, 470)},
}

ALL_BS_WINDOWS = len(WIN_START)


default_timestamp_HUMAN = "2002-10-29 10:00:00"
time_key = f"time_start"

full_screen = "full_screen"

PROTON_VPN = ["proton_vpn_open", "continue_without_registration", "vpn_plus__not_now", "proton_vpn_enable",
              "collapse_all_windows"]
BUTTON_CLOSE_BS_WINDOW = ["button_close_bs_window", "button_close_bs_window__yes"]

APP_INSTALL = {
    "open_play_market": "open_play_market",
    "play_market_first_click": (980, 170),
    "open_loop_searcher_apps": (150, 530),
    "write_text_here": (500, 130),
    "TEXT_TO_WRITE_1": "Pi Network",
    "install_button": "install_button",
    "TEXT_TO_WRITE_2": "Pi Browser",
    "collapse_all_windows": "collapse_all_windows",
    "WAIT": 90,
}

FIRST_OPEN_APP = {
    "app_open": "app_open_pi_network",
    "continue_with_phone_number": "continue_with_phone_number",
    "click_to_write_text_1": (760, 550),
    "write_here_country_phone_number": "+380",
    "select_Ukraine": (840, 600),
    "click_to_write_text_2": (760, 640),
    "phone_number": "",
    "button_send": "button_send",
}

app_open_pi_network = "app_open_pi_network"
button_open_farming = "button_open_farming"
button_start_farming = "button_start_farming"


