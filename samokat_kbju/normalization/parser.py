import re
from typing import Optional

from samokat_kbju.cart.models import CartItem
from samokat_kbju.normalization.models import (
    NormalizedCartItem,
    ParsedPackaging,
    Unit,
)


_UNIT_ALIASES: dict[str, Unit] = {
    "г": Unit.GRAM,
    "гр": Unit.GRAM,
    "кг": Unit.KILOGRAM,
    "мл": Unit.MILLILITER,
    "л": Unit.LITER,
    "шт": Unit.PIECE,
    "штук": Unit.PIECE,
    "шт.": Unit.PIECE,
}


def normalize_text(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").strip().lower().split())


def parse_packaging(raw_text: Optional[str]) -> Optional[ParsedPackaging]:
    if not raw_text:
        return None

    text = normalize_text(raw_text)

    match = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*([a-zA-Zа-яА-Я.]+)", text)
    if not match:
        return None

    raw_value, raw_unit = match.groups()
    unit = _UNIT_ALIASES.get(raw_unit)
    if unit is None:
        return None

    value = float(raw_value.replace(",", "."))

    return ParsedPackaging(
        raw_text=raw_text,
        value=value,
        unit=unit,
    )


def packaging_to_grams(parsed: ParsedPackaging) -> Optional[float]:
    if parsed.unit == Unit.GRAM:
        return parsed.value
    if parsed.unit == Unit.KILOGRAM:
        return parsed.value * 1000
    return None


def packaging_to_milliliters(parsed: ParsedPackaging) -> Optional[float]:
    if parsed.unit == Unit.MILLILITER:
        return parsed.value
    if parsed.unit == Unit.LITER:
        return parsed.value * 1000
    return None


def normalize_cart_item(cart_item: CartItem) -> NormalizedCartItem:
    parsed_packaging = parse_packaging(cart_item.raw_packaging)

    return NormalizedCartItem(
        cart_item=cart_item,
        parsed_packaging=parsed_packaging,
    )