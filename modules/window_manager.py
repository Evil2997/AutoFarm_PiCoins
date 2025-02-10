import pyautogui as pg
from ahk import AHK

from modules.constants import close_all_BS_window
from modules.image_finder import delay, hunt_for_the_button_in_list

ahk = AHK()


def find_manager_window():
    """
    Ищет окно BlueStacks Multi Instance Manager по началу заголовка.
    Возвращает объект окна или None, если не найдено.
    """
    for w in ahk.list_windows():
        if w.title.startswith("BlueStacks Multi Instance Manager"):
            return w
    return None


def activate_manager_window(window, attempts=8):
    """
    Активирует окно BlueStacks Multi Instance Manager несколько раз,
    чтобы AHK гарантированно отобразил окно сверху.
    """
    for _ in range(attempts):
        window.activate()
        delay(0.02, 0.2)


def move_manager_window(window, x=0, y=0):
    """
    Ставит окно Manager в позицию (x, y) на экране.
    """
    window.move(x, y)


def stop_bs_windows():
    """
    Закрывает все окна BlueStacks через интерфейс Manager
    (кликает по кнопкам в определенных координатах).
    """
    manager_win = find_manager_window()
    if manager_win:
        # Активируем окно несколько раз
        for _ in range(8):
            manager_win.activate()
            delay(0.02, 0.2)
        # Кликаем по координатам (для твоей логики)
        for coordinates in close_all_BS_window:
            pg.click(coordinates)
            delay(1.6, 3.2)


def activate_main_window():
    """
    Ищет основное окно BlueStacks (не Manager) и кликает по кнопке 'full_screen',
    если та найдена.
    """
    full_screen = ["full_screen"]
    for win in ahk.list_windows():
        if (
                win.title.startswith("BlueStacks")
                and not win.title.startswith("BlueStacks Multi Instance Manager")
                and not win.title.startswith("BlueStacks-MultiTasks")
        ):
            win.activate()
            hunt_for_the_button_in_list(full_screen, hunt_in_seconds=30)
            break
    delay()
