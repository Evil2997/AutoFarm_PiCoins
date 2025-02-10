import json
import logging
import pathlib


def load_data(file_path: pathlib.Path) -> dict:
    """
    Читает и возвращает данные из JSON-файла.
    Если файл не найден или повреждён, возвращает пустой словарь.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as jf:
            return json.load(jf)
    except FileNotFoundError:
        logging.warning(f"Файл настроек не найден: {file_path}, возвращаем пустой словарь.")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка разбора JSON в файле {file_path}: {e}")
        return {}


def save_data(file_path: pathlib.Path, data: dict) -> None:
    """
    Сохраняет данные словаря 'data' в JSON-файл 'file_path' с отступом = 2.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as jf:
            json.dump(data, jf, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Не удалось сохранить данные в {file_path}: {e}")
