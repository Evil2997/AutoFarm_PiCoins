def get_declension(number: int, forms: list[str]) -> str:
    if 11 <= number % 100 <= 14:
        return forms[2]
    elif number % 10 == 1:
        return forms[0]
    elif 2 <= number % 10 <= 4:
        return forms[1]
    else:
        return forms[2]

def format_elapsed_time(time_end: float, time_start: float) -> str:
    elapsed = time_end - time_start
    days = int(elapsed // (24 * 3600))
    hours = int((elapsed % (24 * 3600)) // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    day_form = get_declension(days, ["день", "дня", "дней"])
    hour_form = get_declension(hours, ["час", "часа", "часов"])
    minute_form = get_declension(minutes, ["минута", "минуты", "минут"])
    second_form = get_declension(seconds, ["секунда", "секунды", "секунд"])
    return (f"Время работы процесса: {days} {day_form}, {hours} {hour_form}, "
            f"{minutes} {minute_form}, {seconds} {second_form}")
