from dataclasses import dataclass
from typing import Optional


@dataclass
class CartItem:
    name: str
    quantity: int

    price_total: Optional[float] = None
    price_per_unit: Optional[float] = None

    raw_packaging: Optional[str] = None  # "500 г", "2 шт", "1 л"

    product_url: Optional[str] = None