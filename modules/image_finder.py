import time
import random
import cv2
import numpy as np
import pyautogui as pg
from PIL import ImageGrab


def delay(min_seconds: float = 1.0, max_seconds: float = 2.0):
    """
    Случайная задержка в диапазоне [min_seconds, max_seconds].
    """
    time.sleep(random.uniform(min_seconds, max_seconds))


def get_image_size(image_path: str) -> tuple[int, int]:
    """
    Возвращает (width, height) изображения.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    height, width, _ = image.shape
    return width, height


def find_template_in_region(
    template_path: str,
    region: tuple[int, int, int, int] = (0, 0, 1920, 1080),
    threshold: float = 0.92,
) -> tuple[int, int] | None:
    """
    Ищет шаблон в указанной области экрана методом cv2.matchTemplate.
    Если найдено совпадение выше threshold, возвращает координаты (x, y) левого верхнего угла; иначе None.
    """
    (x1, y1, x2, y2) = region
    # Делаем скриншот нужной области
    screenshot = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template image not found: {template_path}")

    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        top_left = (max_loc[0] + x1, max_loc[1] + y1)
        return top_left
    return None


def hunt_for_the_button_in_list(
    name_list: list[str],
    hunt_in_seconds: float = 10,
    region: tuple[int, int, int, int] = (0, 0, 1920, 1080),
    threshold: float = 0.92,
    images_dir: str = "Images"
) -> bool:
    """
    В течение hunt_in_seconds пытается найти хотя бы одну картинку из name_list в заданном region.
    Если найдена — кликает и выходит (True). Если время вышло и ничего не нашлось — False.
    """
    time_start = time.time()
    while time.time() - time_start < hunt_in_seconds:
        for name in name_list:
            template_path = f"{images_dir}/{name}.png"
            top_left = find_template_in_region(template_path, region, threshold)
            if top_left:
                width, height = get_image_size(template_path)
                delay(0.2, 0.3)
                # Кликаем по центру найденного шаблона
                pg.click(top_left[0] + width / 2, top_left[1] + height / 2)
                return True
        delay(0.01, 0.1)
    return False


def find_it_and_click_it(
    name_list: list[str],
    region: tuple[int, int, int, int] = (0, 0, 1920, 1080),
    threshold: float = 0.92,
    images_dir: str = "Images"
) -> bool:
    """
    Последовательно ищет шаблоны из name_list. Кликает по первому найденному.
    Если в списке только один элемент, возвращает True (если клик был) или False (если не найден).
    """
    for name in name_list:
        template_path = f"{images_dir}/{name}.png"
        top_left = find_template_in_region(template_path, region, threshold)
        if top_left:
            width, height = get_image_size(template_path)
            delay(0.2, 0.3)
            pg.click(top_left[0] + width / 2, top_left[1] + height / 2)
            if len(name_list) == 1:
                return True
        elif len(name_list) == 1:
            return False
    return True


def cycle_hunter_click(
    name_list: list[str],
    region: tuple[int, int, int, int] = (0, 0, 1920, 1080),
    threshold: float = 0.92,
    images_dir: str = "Images"
) -> None:
    """
    Поочередно ищет каждую картинку из списка (name_list), пока не найдёт,
    кликает, и переходит к следующей.
    """
    for name in name_list:
        template_path = f"{images_dir}/{name}.png"
        while True:
            top_left = find_template_in_region(template_path, region, threshold)
            if top_left:
                width, height = get_image_size(template_path)
                delay(0.2, 0.3)
                pg.click(top_left[0] + width / 2, top_left[1] + height / 2)
                break
            else:
                delay(0.04, 0.2)
        delay(0.8, 1.2)
