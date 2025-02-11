skip_option = ["skip_option"]

connect_to_vpn_AND_open_telegram = [
    "collapse_all_windows", "check_all_windows",
    "clear_all", "ProtonVPN", "ActivateVPN",
    "collapse_all_windows", "Telegram"
]

Telegram = ["Telegram"]

main_group = ["main_group_1", "main_group_2"]

full_screen = ["full_screen"]

close_all_BS_window = [(350, 590), (500, 360)]

WIN_START = {
    "win0": {"cords": (540, 200)},
    "win1": {"cords": (540, 250)},
    "win2": {"cords": (540, 310)},
    "win3": {"cords": (540, 360)},
    "win4": {"cords": (540, 420)},
    "win5": {"cords": (540, 470)},
}

window_numbers = len(WIN_START)

DEFAULT_REGION = (0, 0, 1920, 1080)
DEFAULT_THRESHOLD = 0.92
DEFAULT_IMAGES_DIR = "Images"
DEFAULT_HUNT_TIMEOUT = 10.0
DEFAULT_DELAY_BEFORE_CLICK = (0.2, 0.3)
DEFAULT_DELAY_BETWEEN_CHECKS = (0.01, 0.1)
DEFAULT_DELAY_AFTER_CLICK = (0.8, 1.2)
DEFAULT_CYCLE_CHECK_DELAY = (0.04, 0.2)

# Количество попыток активации окна Manager
MANAGER_ACTIVATION_ATTEMPTS = 8

# Задержки для активации окна Manager (нижняя и верхняя границы)
MANAGER_ACTIVATION_DELAY_SHORT = 0.02
MANAGER_ACTIVATION_DELAY_UPPER = 0.2

# Задержки для кликов при закрытии окон BS
STOP_WINDOW_CLICK_DELAY = 1.6
STOP_WINDOW_CLICK_INTERVAL = 3.2

# Задержка по умолчанию для вызова функции delay() (нижняя и верхняя границы)
DEFAULT_DELAY_MIN = 1.0
DEFAULT_DELAY_MAX = 2.0

ACTIVATION_ITERATIONS = 16
ACTIVATION_MOVE_DELAY_MIN = 0.01
ACTIVATION_MOVE_DELAY_MAX = 0.04
WAIT_AFTER_CLICK_MIN = 30
WAIT_AFTER_CLICK_MAX = 40

SLEEP_IF_NO_MANAGER = 30
SLEEP_BETWEEN_CYCLES = 180

DEFAULT_TIMESTAMP = "2002-10-29 10:00:00"

WIN_START = {
    "win0": {"cords": (540, 200)},
    "win1": {"cords": (540, 250)},
    "win2": {"cords": (540, 310)},
    "win3": {"cords": (540, 360)},
    "win4": {"cords": (540, 420)},
    "win5": {"cords": (540, 470)},
}
