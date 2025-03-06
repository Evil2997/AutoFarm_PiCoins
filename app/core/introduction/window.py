import pyautogui as pg
from ahk import AHK

from app.core.actions.clicker_manager.unified_hunt_click import delay
from app.logs.logger import logger

ahk = AHK()


def find_manager_window():
    for w in ahk.list_windows():
        if w.title.startswith("BlueStacks Multi Instance Manager"):
            move_window(w)
            return w
    logger.error("Окно BlueStacks Multi Instance Manager не найдено.")
    return None


def activate_manager_window(attempts=8):
    manager_win = find_manager_window()
    for _ in range(attempts):
        manager_win.activate()
        delay(0.02, 0.05)


def move_window(window, x=0, y=0):
    window.move(x, y)


def activate_bs_window(
        BS_WINDOW_NUMERIC: int,
        BS_WINDOW_CORDS: tuple[int, int],
        attempts: int = 3,
):
    BS_WINDOW_FOUND = False
    BS_WINDOW_NAME = f"BlueStacks {BS_WINDOW_NUMERIC}"

    activate_manager_window()
    pg.click(BS_WINDOW_CORDS)
    delay(20, 30)
    for _ in range(attempts):
        for win in ahk.list_windows():
            if win.title.startswith(BS_WINDOW_NAME):
                win.activate()
                BS_WINDOW_FOUND = True
                break
        if BS_WINDOW_FOUND:
            break

    if not BS_WINDOW_FOUND:
        logger.error("Основное окно BlueStacks не найдено в activate_main_window.")
        raise Exception("Основное окно BlueStacks не найдено")
    delay()
