# window_manager.py

import pyautogui as pg
from ahk import AHK

from modules.constants import (
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
from modules.image_finder import delay, unified_hunt_click
from modules.logger import logger

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


def activate_main_window():
    main_found = False
    for win in ahk.list_windows():
        if (win.title.startswith("BlueStacks")
                and not win.title.startswith("BlueStacks Multi Instance Manager")
                and not win.title.startswith("BlueStacks-MultiTasks")):
            win.activate()
            unified_hunt_click(full_screen, mode="hunt", timeout=30)
            main_found = True
            logger.info("Основное окно BlueStacks активировано.")
            break
    if not main_found:
        logger.error("Основное окно BlueStacks не найдено в activate_main_window.")
        raise Exception("Основное окно BlueStacks не найдено")
    delay(DEFAULT_DELAY_MIN, DEFAULT_DELAY_MAX)
