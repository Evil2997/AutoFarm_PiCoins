import json
import pathlib

from app.logs.logger import logger


def load_data(file_path: pathlib.Path) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as jf:
            return json.load(jf)
    except FileNotFoundError:
        logger.warning(f"Файл настроек не найден: {file_path}. Возвращаю пустой словарь.")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка разбора JSON в {file_path}: {e}")
        return {}


def save_data(file_path: pathlib.Path, data: dict) -> None:
    try:
        with open(file_path, 'w', encoding='utf-8') as jf:
            json.dump(data, jf, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Не удалось сохранить данные в {file_path}: {e}")
