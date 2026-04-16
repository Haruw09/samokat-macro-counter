from samokat_kbju.normalization.parser import Unit, parse_packaging


def test_parse_grams() -> None:
    result = parse_packaging("50 г")

    assert result is not None
    assert result.value == 50
    assert result.unit == Unit.GRAM


def test_parse_kilograms() -> None:
    result = parse_packaging("1 кг")

    assert result is not None
    assert result.value == 1
    assert result.unit == Unit.KILOGRAM


def test_parse_liters() -> None:
    result = parse_packaging("0.5 л")

    assert result is not None
    assert result.value == 0.5
    assert result.unit == Unit.LITER


def test_parse_pieces() -> None:
    result = parse_packaging("2 шт")

    assert result is not None
    assert result.value == 2
    assert result.unit == Unit.PIECE


def test_parse_invalid_packaging() -> None:
    assert parse_packaging("abc") is None
    assert parse_packaging("") is None
    assert parse_packaging(None) is None