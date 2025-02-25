import time

from utils.constants import APP_OPEN_ICON, PROTON_VPN, ALL_BS_WINDOWS
from utils.logger import logger
from utils.update_cycle_timestamp import update_cycle_timestamp
from utils.unified_hunt_click import unified_hunt_click, delay


def run_cycle(
        BS_WINNODW_NUMERIC,
        BS_WINNODW_COORDS,

):
    logger.info("Запуск цикла: активация окна BlueStacks.")

    logger.info("Запуск ProtonVPN...")
    unified_hunt_click(PROTON_VPN, mode="hunt", timeout=5, threshold=0.9)
    delay(2, 3)

    logger.info("Открытие целевого приложения...")
    unified_hunt_click([APP_OPEN_ICON], mode="hunt", timeout=5, threshold=0.9)
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
        for i in range(len(ALL_BS_WINDOWS)):
            run_cycle()
        logger.info(f"Цикл завершён. Следующий запуск через {CYCLE_INTERVAL} секунд.")
        time.sleep(CYCLE_INTERVAL)
