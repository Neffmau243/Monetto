from decimal import ROUND_HALF_UP, Decimal
from typing import Any

ZERO = Decimal("0.00")
CENT = Decimal("0.01")


def to_decimal(value: Any) -> Decimal:
    if value is None:
        return ZERO
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def money(value: Any) -> Decimal:
    return to_decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def percentage(part: Any, total: Any) -> Decimal:
    total_decimal = to_decimal(total)
    if total_decimal == 0:
        return ZERO
    return ((to_decimal(part) * Decimal("100")) / total_decimal).quantize(
        CENT, rounding=ROUND_HALF_UP
    )
