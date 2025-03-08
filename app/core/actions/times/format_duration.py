from app.core.actions.times.get_declension import get_declension


def format_duration(seconds: int) -> str:
    days = seconds // (24 * 3600)
    remainder = seconds % (24 * 3600)
    hours = remainder // 3600
    remainder %= 3600
    minutes = remainder // 60
    sec = remainder % 60
    day_form = get_declension(days, ["день", "дня", "дней"])
    hour_form = get_declension(hours, ["час", "часа", "часов"])
    minute_form = get_declension(minutes, ["минута", "минуты", "минут"])
    second_form = get_declension(sec, ["секунда", "секунды", "секунд"])
    return f"{days} {day_form}, {hours} {hour_form}, {minutes} {minute_form}, {sec} {second_form}"
