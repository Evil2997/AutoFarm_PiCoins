import pyautogui as pg

from app.core.actions.clicker_manager.unified_hunt_click import unified_hunt_click
from app.core.actions.find_template_in_region import find_template_in_region
from app.core.app_install import app_install
from app.core.checker.check_consent_on_screen import check_consent_on_screen
from app.core.constants import PROTON_VPN, DEFAULT_THRESHOLD, BUTTON_CLOSE_BS_WINDOW, SETTINGS_FILE, \
    app_open_pi_network, button_open_farming, button_start_farming, full_screen, button_open_farming_by_cords, \
    TICK_THE_BOX_VERIFICATION
from app.core.first_open_app import first_open_app
from app.core.introduction.window import activate_bs_window
from app.core.managers.delay import delay
from app.core.managers.time_checker import timer_update
from app.logs.logger import logger
from app.main.run_farm_app import run_farm_app


def full_cycle_in_window(
        BS_WINDOW_NUMERIC,
        BS_WINDOW_CORDS,
):
    activate_bs_window(
        BS_WINDOW_NUMERIC=BS_WINDOW_NUMERIC,
        BS_WINDOW_CORDS=BS_WINDOW_CORDS,
    )
    delay(2, 3)

    unified_hunt_click(full_screen, timeout=30, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    for name in PROTON_VPN:
        unified_hunt_click(name=name, timeout=5, threshold=DEFAULT_THRESHOLD)
        delay(2, 3)

    if not find_template_in_region(name=app_open_pi_network, threshold=DEFAULT_THRESHOLD):
        app_install()
        first_open_app()
        # Передаем конкретные данные для регистрации
        raise SystemExit

    unified_hunt_click(name=app_open_pi_network, timeout=5, threshold=DEFAULT_THRESHOLD)
    delay(40, 45)

    RUN_FARM_APP = run_farm_app()

    if check_consent_on_screen():
        for _ in range(2):
            unified_hunt_click(name=TICK_THE_BOX_VERIFICATION["tick_the_box"], timeout=20, threshold=DEFAULT_THRESHOLD)
            delay(4, 5)
        unified_hunt_click(name=TICK_THE_BOX_VERIFICATION["button_send"], timeout=20, threshold=DEFAULT_THRESHOLD)
        delay(4, 5)
        pg.click(935, 350)
        delay(4, 5)

    if not RUN_FARM_APP:
        run_farm_app()

    for name in BUTTON_CLOSE_BS_WINDOW:
        unified_hunt_click(name=name, timeout=15, threshold=0.85)
        delay(2, 3)

    timer_update(
        path_to_settings_file=SETTINGS_FILE,
        window_numeric=BS_WINDOW_NUMERIC,
    )
    logger.info(f"Был завершен полный цикл для BlueStacks {BS_WINDOW_NUMERIC}")
