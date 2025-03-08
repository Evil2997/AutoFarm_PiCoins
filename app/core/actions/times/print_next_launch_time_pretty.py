from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.core.actions.times.format_duration import format_duration
from app.core.actions.times.time_until_next_launch import time_until_next_launch
from app.core.constants import ONE_DAY, ALL_BS_WINDOWS, SETTINGS_FILE


def print_next_launch_time_pretty(
        file_path: str = SETTINGS_FILE,
        num_windows: int = ALL_BS_WINDOWS,
        interval_seconds: int = ONE_DAY,
) -> int:
    console = Console()
    seconds_until_next = time_until_next_launch(file_path, num_windows, interval_seconds)
    pretty_time = format_duration(seconds_until_next)

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Параметр", style="dim", width=30)
    table.add_column("Значение", justify="right")
    table.add_row("Следующий запуск через", pretty_time)

    panel = Panel(table, title="Статус приложения", border_style="green")
    console.print(panel)

    return seconds_until_next
