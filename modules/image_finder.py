# image_finder.py

import random
import time

import cv2
import numpy as np
import pyautogui as pg
from PIL import ImageGrab

from constants import (
    DEFAULT_REGION,
    DEFAULT_THRESHOLD,
    DEFAULT_IMAGES_DIR,
    DEFAULT_HUNT_TIMEOUT,
    DEFAULT_DELAY_BEFORE_CLICK,
    DEFAULT_DELAY_BETWEEN_CHECKS,
    DEFAULT_DELAY_AFTER_CLICK,
    DEFAULT_CYCLE_CHECK_DELAY,
)
from modules.logger import logger
from modules.models.click_modes import ModeEnum


def delay(min_seconds: float, max_seconds: float):
    time.sleep(random.uniform(min_seconds, max_seconds))


def get_image_size(image_path: str) -> tuple[int, int]:
    image = cv2.imread(image_path)
    if image is None:
        logger.error(f"Image not found: {image_path}")
        raise FileNotFoundError(f"Image not found: {image_path}")
    height, width, _ = image.shape
    return width, height


def find_template_in_region(name: str, region: tuple[int, int, int, int], threshold: float, images_dir: str) -> tuple[
                                                                                                                    int, int] | None:
    template_path = f"{images_dir}/{name}.png"
    (x1, y1, x2, y2) = region
    screenshot = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        logger.error(f"Template image not found: {template_path}")
        raise FileNotFoundError(f"Template image not found: {template_path}")
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        top_left = (max_loc[0] + x1, max_loc[1] + y1)
        logger.info(f"Found template '{name}' (confidence: {max_val}) at {top_left}")
        return top_left
    return None


def _attempt_click(
        name: str,
        region: tuple[int, int, int, int],
        threshold: float,
        images_dir: str,
        delay_before_click: tuple[float, float]
) -> bool:
    pos = find_template_in_region(name, region, threshold, images_dir)
    if pos:
        image_path = f"{images_dir}/{name}.png"
        w, h = get_image_size(image_path)
        delay(*delay_before_click)
        pg.click(pos[0] + w / 2, pos[1] + h / 2)
        logger.info(f"Clicked on '{name}' at {pos}")
        return True
    return False


def unified_hunt_click(
        name_list: list[str],
        mode: str = "hunt",
        timeout: float | None = DEFAULT_HUNT_TIMEOUT,
        region: tuple[int, int, int, int] = DEFAULT_REGION,
        threshold: float = DEFAULT_THRESHOLD,
        images_dir: str = DEFAULT_IMAGES_DIR,
        delay_before_click: tuple[float, float] = DEFAULT_DELAY_BEFORE_CLICK,
        delay_between_checks: tuple[float, float] = DEFAULT_DELAY_BETWEEN_CHECKS,
        delay_after_click: tuple[float, float] = DEFAULT_DELAY_AFTER_CLICK,
) -> bool:
    if mode == ModeEnum.hunt:
        start_time = time.time()
        while True:
            for name in name_list:
                if _attempt_click(name, region, threshold, images_dir, delay_before_click):
                    return True
            if timeout is not None and (time.time() - start_time > timeout):
                logger.info("Timeout reached in hunt mode.")
                return False
            delay(*delay_between_checks)

    elif mode == ModeEnum.once:
        for name in name_list:
            if _attempt_click(name, region, threshold, images_dir, delay_before_click):
                return True
        logger.info("No template found in once mode.")
        return False

    elif mode == ModeEnum.cycle:
        for name in name_list:
            while not _attempt_click(name, region, threshold, images_dir, delay_before_click):
                delay(*DEFAULT_CYCLE_CHECK_DELAY)
            delay(*delay_after_click)
        return True

    else:
        logger.error(f"Unexpected mode: {mode}")
        raise ValueError(f"Unexpected mode: {mode}")
