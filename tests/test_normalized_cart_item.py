from samokat_kbju.cart.models import CartItem
from samokat_kbju.normalization.models import NormalizedCartItem, Unit
from samokat_kbju.normalization.parser import normalize_cart_item


def test_normalize_cart_item_with_packaging() -> None:
    cart_item = CartItem(
        name="Клубника",
        quantity=1,
        price_current=349.0,
        price_old=399.0,
        raw_packaging="250 г",
    )

    result = normalize_cart_item(cart_item)

    assert isinstance(result, NormalizedCartItem)
    assert result.cart_item is cart_item
    assert result.parsed_packaging is not None
    assert result.parsed_packaging.value == 250
    assert result.parsed_packaging.unit == Unit.GRAM


def test_normalize_cart_item_without_packaging() -> None:
    cart_item = CartItem(
        name="Что-то без фасовки",
        quantity=1,
        raw_packaging=None,
    )

    result = normalize_cart_item(cart_item)

    assert result.cart_item is cart_item
    assert result.parsed_packaging is None