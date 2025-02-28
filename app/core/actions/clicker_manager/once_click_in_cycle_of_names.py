from app.core.actions.attempt_click import attempt_click
from app.core.constants import (
    DEFAULT_REGION,
    DEFAULT_THRESHOLD,
)
from app.core.managers.delay import delay


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
