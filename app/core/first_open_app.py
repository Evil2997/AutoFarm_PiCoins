import pyautogui as pg

from app.core.actions.clicker_manager.unified_hunt_click import unified_hunt_click
from app.core.constants import FIRST_OPEN_APP, DEFAULT_THRESHOLD
from app.core.managers.delay import delay


def first_open_app():
    unified_hunt_click(FIRST_OPEN_APP["app_open"], timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(25, 30)

    unified_hunt_click(FIRST_OPEN_APP["continue_with_phone_number"], timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(3, 4)

    pg.click(FIRST_OPEN_APP["click_to_write_text_1"])
    delay(2, 3)

    pg.write(FIRST_OPEN_APP["write_here_country_phone_number"], interval=0.4)
    delay(2, 3)
    pg.click(FIRST_OPEN_APP["select_Ukraine"])
    delay(2, 3)

    pg.click(FIRST_OPEN_APP["click_to_write_text_2"])
    delay(2, 3)
    pg.write(FIRST_OPEN_APP["phone_number"], interval=0.4)
    delay(2, 3)

    unified_hunt_click(FIRST_OPEN_APP["continue_with_phone_number"], timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(3, 4)
