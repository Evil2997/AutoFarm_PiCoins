import pytesseract.pytesseract
import json
import os



def setup_tesseract(search_paths=['C:\\'], config_file_name='tesseract_config.json'):
    # search_paths = ['C:\\', 'D:\\', 'E:\\']

    # Функция для загрузки сохраненного пути
    def load_tesseract_path():
        if os.path.exists(config_file_name):
            with open(config_file_name, 'r') as file:
                config = json.load(file)
                tesseract_path = config.get('tesseract_path')
                if tesseract_path and os.path.exists(tesseract_path):
                    return tesseract_path
        return None

    # Функция для сохранения пути
    def save_tesseract_path(tesseract_path):
        with open(config_file_name, 'w') as file:
            json.dump({'tesseract_path': tesseract_path}, file, indent=2)

    # Сначала проверяем сохраненный путь
    tesseract_path = load_tesseract_path()
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        return tesseract_path

    # Ищем tesseract.exe на указанных дисках
    for path in search_paths:
        try:
            for root, dirs, files in os.walk(path):
                if 'tesseract.exe' in files:
                    tesseract_path = os.path.join(root, 'tesseract.exe')
                    pytesseract.pytesseract.tesseract_cmd = tesseract_path
                    save_tesseract_path(tesseract_path)
                    return tesseract_path
        except (FileNotFoundError, PermissionError):
            continue

    raise TesseractFileNotFoundError

class TesseractFileNotFoundError(FileNotFoundError):
    pass