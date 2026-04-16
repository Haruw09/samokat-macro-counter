from dataclasses import dataclass
from typing import Optional


@dataclass
class CartItem:
    name: str
    quantity: int
    price_current: Optional[float] = None
    price_old: Optional[float] = None
    raw_packaging: Optional[str] = None
    product_url: Optional[str] = None