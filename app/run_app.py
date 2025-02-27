import time

from app.core.actions.full_cycle_in_window import full_cycle_in_window
from app.core.constants import ALL_BS_WINDOWS, WIN_START, CYCLE_INTERVAL
from app.logs.logger import logger


def run_app():
    while True:
        for i in range(ALL_BS_WINDOWS):
            BS_WINDOW_NUMERIC = i
            BS_WINDOW_CORDS = WIN_START[f"win{i}"]["cords"]
            full_cycle_in_window(BS_WINDOW_NUMERIC=BS_WINDOW_NUMERIC, BS_WINDOW_CORDS=BS_WINDOW_CORDS)
        logger.info(f"Цикл завершён. Следующий запуск через {CYCLE_INTERVAL} секунд.")
        time.sleep(CYCLE_INTERVAL)
