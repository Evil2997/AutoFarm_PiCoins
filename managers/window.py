import pyautogui as pg
from ahk import AHK

from utils.constants import (
    close_all_BS_window,
    MANAGER_ACTIVATION_ATTEMPTS,
    MANAGER_ACTIVATION_DELAY_SHORT,
    MANAGER_ACTIVATION_DELAY_UPPER,
    STOP_WINDOW_CLICK_DELAY,
    STOP_WINDOW_CLICK_INTERVAL,
    DEFAULT_DELAY_MIN,
    DEFAULT_DELAY_MAX,
    full_screen,
)
from utils.logger import logger
from utils.unified_hunt_click import delay, unified_hunt_click

ahk = AHK()


def find_manager_window():
    for w in ahk.list_windows():
        if w.title.startswith("BlueStacks Multi Instance Manager"):
            logger.info("Найдено окно BlueStacks Multi Instance Manager.")
            return w
    logger.error("Окно BlueStacks Multi Instance Manager не найдено.")
    return None


def activate_manager_window(window, attempts=MANAGER_ACTIVATION_ATTEMPTS):
    for _ in range(attempts):
        window.activate()
        delay(MANAGER_ACTIVATION_DELAY_SHORT, MANAGER_ACTIVATION_DELAY_UPPER)
    logger.info("Окно Manager активировано.")


def move_manager_window(window, x=0, y=0):
    window.move(x, y)
    logger.info(f"Окно Manager перемещено в позицию ({x}, {y}).")


def stop_bs_windows():
    manager_win = find_manager_window()
    if manager_win is None:
        logger.error("Окно Manager не найдено в stop_bs_windows.")
        raise Exception("Окно Manager не найдено")
    for _ in range(MANAGER_ACTIVATION_ATTEMPTS):
        manager_win.activate()
        delay(MANAGER_ACTIVATION_DELAY_SHORT, MANAGER_ACTIVATION_DELAY_UPPER)
    for coordinates in close_all_BS_window:
        pg.click(coordinates)
        delay(STOP_WINDOW_CLICK_DELAY, STOP_WINDOW_CLICK_INTERVAL)
    logger.info("Окна BS закрыты.")


def activate_this_bs_window(BS_WINDOW_NUMERIC: int):
    BS_WINDOW_FOUND = False
    BS_WINDOW_NAME = f"BlueStacks {BS_WINDOW_NUMERIC}"
    for win in ahk.list_windows():
        if win.title.startswith(BS_WINDOW_NAME):
            win.activate()
            unified_hunt_click(full_screen, mode="hunt", timeout=30)
            BS_WINDOW_FOUND = True
            logger.info("Основное окно BlueStacks активировано.")
            break
    if not BS_WINDOW_FOUND:
        logger.error("Основное окно BlueStacks не найдено в activate_main_window.")
        raise Exception("Основное окно BlueStacks не найдено")
    delay(DEFAULT_DELAY_MIN, DEFAULT_DELAY_MAX)
