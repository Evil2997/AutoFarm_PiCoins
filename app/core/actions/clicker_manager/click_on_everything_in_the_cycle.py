from app.core.actions.attempt_click import attempt_click
from app.core.constants import (
    DEFAULT_REGION,
    DEFAULT_THRESHOLD,
)
from app.core.models.not_found_error import NotFoundError
from app.logs.logger import logger


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
