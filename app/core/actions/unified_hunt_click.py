import time

from app.core.actions.attempt_click import attempt_click
from app.core.constants import (
    DEFAULT_REGION,
    DEFAULT_THRESHOLD,
    DEFAULT_HUNT_TIMEOUT,
)
from app.core.managers.delay import delay
from app.core.models.click_modes import ModeEnum
from app.core.models.not_found_error import NotFoundError
from app.logs.logger import logger


def unified_hunt_click(
        name_list: list[str],
        timeout: float | None = DEFAULT_HUNT_TIMEOUT,
        region: tuple[int, int, int, int] = DEFAULT_REGION,
        threshold: float = DEFAULT_THRESHOLD,
) -> None:
    for name in name_list:
        start_time = time.time()
        while not attempt_click(
                    name=name,
                    region=region,
                    threshold=threshold,
            ):
            delay(0.2, 0.5)
            if timeout is not None and (time.time() - start_time > timeout):
                logger.info("Timeout reached in hunt mode.")
                break
            delay(0.2, 0.5)

def click_on_everything_in_the_cycle(
        name_list: list[str],
        region: tuple[int, int, int, int] = DEFAULT_REGION,
        threshold: float = DEFAULT_THRESHOLD,
) -> bool | None:

    for name in name_list:
        if attempt_click(
                name=name,
                region=region,
                threshold=threshold,
        ):
            return True
    logger.info("No template found in once mode.")
    raise NotFoundError


def once_click_in_cycle_of_names(
        name_list: list[str],
        region: tuple[int, int, int, int] = DEFAULT_REGION,
        threshold: float = DEFAULT_THRESHOLD,
) -> None:
    for name in name_list:
        while not attempt_click(
                name=name,
                region=region,
                threshold=threshold,
        ):
            delay(0.2, 0.5)
            break
        delay(0.2, 0.5)
