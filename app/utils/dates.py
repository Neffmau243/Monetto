from datetime import date

from app.exceptions.domain import ValidationError


def month_start(value: date) -> date:
    return value.replace(day=1)


def next_month(value: date) -> date:
    year = value.year + (1 if value.month == 12 else 0)
    month = 1 if value.month == 12 else value.month + 1
    return date(year, month, 1)


def parse_month(value: str | None) -> date:
    if value is None:
        return month_start(date.today())
    try:
        year_text, month_text = value.split("-", maxsplit=1)
        parsed = date(int(year_text), int(month_text), 1)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Month must use YYYY-MM format") from exc
    return parsed


def month_bounds(value: date) -> tuple[date, date]:
    start = month_start(value)
    return start, next_month(start)


def subtract_months(value: date, count: int) -> date:
    month_index = value.year * 12 + (value.month - 1) - count
    return date(month_index // 12, month_index % 12 + 1, 1)


def iter_months(start: date, count: int) -> list[date]:
    months: list[date] = []
    current = month_start(start)
    for _ in range(count):
        months.append(current)
        current = next_month(current)
    return months
