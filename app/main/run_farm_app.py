import pyautogui as pg

from app.core.actions.clicker_manager.unified_hunt_click import unified_hunt_click
from app.core.constants import (
    button_start_farming,
    button_open_farming_by_cords,
    button_open_farming,
    DEFAULT_THRESHOLD,
)
from app.core.managers.delay import delay
from app.logs.logger import logger


def run_farm_app() -> bool:
    if not unified_hunt_click(name=button_open_farming, timeout=15, threshold=DEFAULT_THRESHOLD):
        pg.click(button_open_farming_by_cords)
    delay(14, 15)
    if unified_hunt_click(name=button_start_farming, timeout=15, threshold=DEFAULT_THRESHOLD):
        delay(12, 13)
        return True
    delay(12, 13)
    return False
