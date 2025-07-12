from datetime import datetime
from zoneinfo import ZoneInfo


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
    hour = date.strftime("%H:%M")

    return f"{day} de {month} a las {hour}"
