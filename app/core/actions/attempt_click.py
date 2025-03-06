import pyautogui as pg

from app.core.actions.find_template_in_region import find_template_in_region
from app.core.actions.get_image_size import get_image_size
from app.core.constants import IMAGE_PATHS
from app.core.managers.delay import delay
from app.logs.logger import logger


def attempt_click(
        name: str,
        region: tuple[int, int, int, int],
        threshold: float,
) -> bool:
    pos = find_template_in_region(
        name=name,
        region=region,
        threshold=threshold
    )
    if pos:
        image_path = str(IMAGE_PATHS / f"{name}.png")
        w, h = get_image_size(image_path)
        delay(0.2, 0.5)
        pg.click(pos[0] + w / 2, pos[1] + h / 2)
        return True
    return False
