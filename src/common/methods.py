from datetime import timedelta
from typing import Optional


def merge_dicts(a: dict, b: dict) -> dict:
    for key, value in b.items():
        if key in a and isinstance(a[key], dict) and isinstance(value, dict):
            a[key] = merge_dicts(a[key], value)
        else:
            a[key] = value
    return a


def add_optionals_to_dict(original: Optional[dict] = None, **optionals) -> dict:
    filled_dict = original.copy() if original else {}
    filtered_optionals = {k: v for k, v in optionals.items() if v is not None}
    filled_dict.update(**filtered_optionals)
    return filled_dict


def format_timedelta(delta: timedelta) -> str:
    template = "{days} дней {hours} час(ов) {minutes} минут(а)"
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return template.format(days=days, hours=hours, minutes=minutes)


def remove_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
