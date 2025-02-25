import time

from managers.window import activate_this_bs_window
from utils.constants import APP_OPEN_ICON, PROTON_VPN, ALL_BS_WINDOWS, WIN_START, DEFAULT_THRESHOLD
from utils.logger import logger
from utils.update_cycle_timestamp import update_cycle_timestamp
from utils.unified_hunt_click import unified_hunt_click, delay


def run_cycle(
        BS_WINDOW_NUMERIC,
        BS_WINDOW_CORDS,

):
    logger.info("Запуск цикла: активация окна BlueStacks.")
    activate_this_bs_window(BS_WINDOW_NUMERIC=BS_WINDOW_NUMERIC)
    logger.info("Запуск ProtonVPN...")
    unified_hunt_click(PROTON_VPN, mode="hunt", timeout=5, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    logger.info("Открытие целевого приложения...")
    unified_hunt_click([APP_OPEN_ICON], mode="hunt", timeout=5, threshold=DEFAULT_THRESHOLD)
    delay(2, 3)

    perform_app_actions()

    update_cycle_timestamp()

    from managers.window import stop_bs_windows
    stop_bs_windows()


def perform_app_actions():
    logger.info("Выполнение действий внутри приложения (заглушка).")
    # Пример:
    # unified_hunt_click(["action_icon1"], mode="hunt", timeout=5, threshold=0.9)
    # delay(1, 2)
    # unified_hunt_click(["action_icon2"], mode="hunt", timeout=5, threshold=0.9)
    pass


if __name__ == '__main__':
    CYCLE_INTERVAL = 24 * 60 * 60  # 24 часа
    while True:
        for i in range(ALL_BS_WINDOWS):
            BS_WINDOW_NUMERIC = i
            BS_WINDOW_CORDS = WIN_START[f"win{i}"]["cords"]
            run_cycle(BS_WINDOW_NUMERIC=BS_WINDOW_NUMERIC, BS_WINDOW_CORDS=BS_WINDOW_CORDS)
        logger.info(f"Цикл завершён. Следующий запуск через {CYCLE_INTERVAL} секунд.")
        time.sleep(CYCLE_INTERVAL)
