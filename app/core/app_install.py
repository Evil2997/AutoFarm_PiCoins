import time

import pyautogui as pg

from app.core.actions.clicker_manager.unified_hunt_click import unified_hunt_click
from app.core.constants import DEFAULT_THRESHOLD, APP_INSTALL
from app.core.managers.delay import delay



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
    pg.press("enter")
    delay(2, 3)

    unified_hunt_click(APP_INSTALL["install_button"], timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    pg.click(APP_INSTALL["write_text_here"])
    delay(2, 3)

    for _ in range(len(APP_INSTALL["TEXT_TO_WRITE_1"])):
        pg.press("backspace")
        delay(0.01, 0.02)
    delay(2, 3)

    pg.write(APP_INSTALL["TEXT_TO_WRITE_2"], interval=0.4)
    delay(2, 3)
    pg.press("enter")
    delay(2, 3)

    unified_hunt_click(APP_INSTALL["install_button"], timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    unified_hunt_click(APP_INSTALL["collapse_all_windows"], timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    time.sleep(APP_INSTALL["WAIT"])