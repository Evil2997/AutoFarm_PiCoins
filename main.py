import time

from app.core.managers.time_formatter import format_elapsed_time
from app.logs.logger import logger
from app.run_app import run_app

if __name__ == '__main__':
    start_time = time.time()

    try:
        run_app()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.info(f"Работа приложения была прервана из за ошибки:\n {e}")

    end_time = time.time()
    print_end_time = format_elapsed_time(end_time, start_time)

    logger.info(print_end_time)
