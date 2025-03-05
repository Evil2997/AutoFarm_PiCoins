import json
import os
import pathlib

import pytesseract.pytesseract

from app.core.constants import tesseract_config, disk_paths


def setup_tesseract(search_paths=disk_paths, config_file_name: pathlib.Path = tesseract_config):
    def load_tesseract_path():
        if os.path.exists(config_file_name):
            with open(config_file_name, 'r') as file:
                config = json.load(file)
                tesseract_path = config.get('tesseract_path')
                if tesseract_path and os.path.exists(tesseract_path):
                    return tesseract_path
        return None

    def save_tesseract_path(tesseract_path):
        with open(config_file_name, 'w') as file:
            json.dump({'tesseract_path': tesseract_path}, file, indent=2)

    tesseract_path = load_tesseract_path()
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        return tesseract_path

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
