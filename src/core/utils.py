import logging
from datetime import datetime
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


def format_date(date: datetime) -> str:
    date = date.astimezone(ZoneInfo("America/Lima"))
    months = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre",
    }

    day = date.strftime("%d")
    month = months[date.month]
    hour_is_default = all([date.minute == 0, date.second == 0, date.microsecond == 0])
    if hour_is_default:
        return f"{day} de {month}"
    else:
        hour = date.strftime("%H:%M")
        return f"{day} de {month} a las {hour}"


def get_current_time() -> str:
    lima_time = datetime.now(ZoneInfo("America/Lima"))
    return lima_time.strftime("%Y-%m-%d %H:%M:%S")
