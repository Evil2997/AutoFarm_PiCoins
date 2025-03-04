import pyautogui as pg

from app.core.actions.clicker_manager.unified_hunt_click import unified_hunt_click
from app.core.actions.find_template_in_region import find_template_in_region
from app.core.app_install import app_install
from app.core.constants import PROTON_VPN, DEFAULT_THRESHOLD, BUTTON_CLOSE_BS_WINDOW, SETTINGS_FILE, \
    app_open_pi_network, button_open_farming, button_start_farming, full_screen, button_open_farming_by_cords
from app.core.first_open_app import first_open_app
from app.core.introduction.window import activate_bs_window
from app.core.managers.delay import delay
from app.core.managers.time_checker import timer_update
from app.logs.logger import logger


def full_cycle_in_window(
        BS_WINDOW_NUMERIC,
        BS_WINDOW_CORDS,
):
    logger.info("Активация окна BlueStacks...")
    activate_bs_window(
        BS_WINDOW_NUMERIC=BS_WINDOW_NUMERIC,
        BS_WINDOW_CORDS=BS_WINDOW_CORDS,
    )
    delay(2, 3)

    unified_hunt_click(full_screen, timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    logger.info("Инициализация и запуск VPN клиента ProtonVPN...")
    for name in PROTON_VPN:
        unified_hunt_click(name=name, timeout=5, threshold=DEFAULT_THRESHOLD)
        delay(2, 3)

    if not find_template_in_region(name=app_open_pi_network, threshold=DEFAULT_THRESHOLD):
        app_install()
        first_open_app()
        # Передаем конкретные данные для регистрации
        raise SystemExit

    logger.info("Открытие целевого приложения...")
    unified_hunt_click(name=app_open_pi_network, timeout=5, threshold=DEFAULT_THRESHOLD)
    delay(10, 15)

    logger.info("Запускаю цикл фарма...")
    if not unified_hunt_click(name=button_open_farming, timeout=5, threshold=DEFAULT_THRESHOLD):
        pg.click(button_open_farming_by_cords)
    delay(2, 3)
    unified_hunt_click(name=button_start_farming, timeout=5, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    logger.info("Закрытие текущего окна BlueStacks...")
    for name in BUTTON_CLOSE_BS_WINDOW:
        unified_hunt_click(name=name, timeout=15, threshold=0.85)
        delay(2, 3)

    timer_update(
        path_to_settings_file=SETTINGS_FILE,
        window_numeric=BS_WINDOW_NUMERIC,
    )
