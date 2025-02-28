import time

import pyautogui as pg

from app.core.actions.clicker_manager.unified_hunt_click import unified_hunt_click
from app.core.constants import DEFAULT_THRESHOLD
from app.core.managers.delay import delay

APP_INSTALL = {
    "open_play_market": ["open_play_market"],
    "play_market_first_click": (980, 170),
    "open_loop_searcher_apps": (150, 530),
    "write_text_here": (500, 130),
    "TEXT_TO_WRITE_1": "Pi Network",
    "install_button": ["install_button"],
    "TEXT_TO_WRITE_2": "Pi Browser",
    "collapse_all_windows": ["collapse_all_windows"],
    "WAIT": 180,
}


def app_install():
    unified_hunt_click(APP_INSTALL["open_play_market"], timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(4, 5)

    pg.click(APP_INSTALL["play_market_first_click"])
    delay(2, 3)

    pg.click(APP_INSTALL["open_loop_searcher_apps"])
    delay(2, 3)

    pg.click(APP_INSTALL["write_text_here"])
    delay(2, 3)

    pg.write(APP_INSTALL["TEXT_TO_WRITE_1"], interval=0.4)
    delay(2, 3)

    unified_hunt_click(APP_INSTALL["install_button"], timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    pg.click(APP_INSTALL["write_text_here"])
    delay(2, 3)

    pg.write(APP_INSTALL["TEXT_TO_WRITE_1"], interval=0.4)
    delay(2, 3)

    unified_hunt_click(APP_INSTALL["install_button"], timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    time.sleep(APP_INSTALL["WAIT"])