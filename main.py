import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.core.actions.times.format_elepset_time import format_elapsed_time
from app.run_app import run_app

if __name__ == '__main__':
    start_time = time.time()

    try:
        run_app()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # Можно также использовать rich для красивого вывода ошибок, если потребуется
        print(f"Работа приложения была прервана из-за ошибки:\n{e}")

    end_time = time.time()
    elapsed_time_str = format_elapsed_time(start_time, end_time)

    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Показатель", style="dim", width=30)
    table.add_column("Значение", justify="right")
    table.add_row("Общее время работы", elapsed_time_str)
    panel = Panel(table, title="Статистика завершения", border_style="red")
    console.print(panel)
