import json
import time

from constants import SETTINGS_FILE
from logger import logger


def update_cycle_timestamp():
    """
    Обновляем JSON-файл, записывая текущее время как отметку выполненного цикла.
    """
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
    except FileNotFoundError:
        data = {}

    data["last_cycle"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    with open(SETTINGS_FILE, 'w', encoding='utf-8') as jf:
        json.dump(data, jf, indent=2, ensure_ascii=False)

    logger.info("Время цикла обновлено в Settings.json.")
