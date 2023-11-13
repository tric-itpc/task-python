def seconds_to_time(seconds: str) -> str:
    """Перевод секунд в месяцы/дни/часы/секунды."""

    seconds_in_minute = 60
    seconds_in_hour = 3600
    seconds_in_day = 86400
    seconds_in_month = 2629746  # среднее количество
    seconds = int(seconds)

    months = seconds // seconds_in_month
    seconds -= months * seconds_in_month

    days = seconds // seconds_in_day
    seconds -= days * seconds_in_day

    hours = seconds // seconds_in_hour
    seconds -= hours * seconds_in_hour

    minutes = seconds // seconds_in_minute
    seconds -= minutes * seconds_in_minute

    result = (
        f'{months} месяцев, {hours} часов, {minutes} минут, '
        f'{seconds} секунд')
    return result
