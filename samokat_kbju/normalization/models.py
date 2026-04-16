from dataclasses import dataclass
from enum import Enum
from typing import Optional

from samokat_kbju.cart.models import CartItem


class Unit(str, Enum):
    GRAM = "g"
    KILOGRAM = "kg"
    MILLILITER = "ml"
    LITER = "l"
    PIECE = "piece"


@dataclass
class ParsedPackaging:
    raw_text: str
    value: float
    unit: Unit


@dataclass
class NormalizedCartItem:
    cart_item: CartItem
    parsed_packaging: Optional[ParsedPackaging] = None