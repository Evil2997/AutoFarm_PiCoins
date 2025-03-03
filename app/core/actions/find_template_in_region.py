import pathlib

import cv2
import numpy as np
from PIL import ImageGrab

from app.core.constants import IMAGE_PATHS, DEFAULT_REGION, DEFAULT_THRESHOLD
from app.logs.logger import logger


def find_template_in_region(
        name: str,
        region: tuple[int, int, int, int] = DEFAULT_REGION,
        threshold: float = DEFAULT_THRESHOLD,
) -> tuple[int, int] | None:
    template_path = str(IMAGE_PATHS / f"{name}.png")
    (x1, y1, x2, y2) = region
    screenshot = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        logger.error(f"Template image not found: {template_path}")
        raise FileNotFoundError(f"Template image not found: {template_path}")
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    if max_val >= threshold:
        top_left = (max_loc[0] + x1, max_loc[1] + y1)
        logger.info(f"Found template '{name}' (confidence: {max_val}) at {top_left}")
        return top_left
    return None
