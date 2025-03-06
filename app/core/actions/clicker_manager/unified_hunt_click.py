import time

from app.core.actions.attempt_click import attempt_click
from app.core.constants import (
    DEFAULT_REGION,
    DEFAULT_THRESHOLD,
)
from app.core.managers.delay import delay
from app.logs.logger import logger


def unified_hunt_click(
        name: str,
        timeout: float | None = 10,
        region: tuple[int, int, int, int] = DEFAULT_REGION,
        threshold: float = DEFAULT_THRESHOLD,
) -> bool:
        start_time = time.time()
        while not attempt_click(
                name=name,
                region=region,
                threshold=threshold,
        ):
            delay(0.2, 0.5)
            if timeout is not None and (time.time() - start_time > timeout):
                break
            delay(0.2, 0.5)
        else:
            return True
        return False