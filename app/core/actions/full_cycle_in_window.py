from app.core.actions.unified_hunt_click import unified_hunt_click
from app.core.constants import PROTON_VPN, DEFAULT_THRESHOLD, APP_OPEN_ICON, BUTTON_CLOSE_BS_WINDOW, full_screen
from app.core.introduction.window import activate_bs_window
from app.core.managers.delay import delay
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
    unified_hunt_click(PROTON_VPN, timeout=5, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    # автоматически ищем окно приложения, если его нет - скачиваем и регистрируемся.

    logger.info("Открытие целевого приложения...")
    unified_hunt_click(APP_OPEN_ICON, timeout=5, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    logger.info("Закрытие текущего окна BlueStacks...")
    unified_hunt_click(BUTTON_CLOSE_BS_WINDOW, timeout=5, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    # TODO: Создать функцию что бы обновить время
