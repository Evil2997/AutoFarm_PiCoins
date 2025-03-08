import time

from app.core.actions.times.format_duration import format_duration


def format_elapsed_time(start_time: float, end_time: float = None) -> str:
    if end_time is None:
        end_time = time.time()
    elapsed_seconds = int(end_time - start_time)
    return format_duration(elapsed_seconds)
