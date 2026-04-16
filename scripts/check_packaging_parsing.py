from samokat_kbju.normalization.parser import parse_packaging


def main() -> None:
    samples = [
        "50 г",
        "330 г",
        "130 г",
        "1 кг",
        "0.5 л",
        "2 шт",
        "3 штук",
        "250 мл",
        None,
        "",
        "abc",
    ]

    for sample in samples:
        result = parse_packaging(sample)
        print(f"{sample!r} -> {result}")


if __name__ == "__main__":
    main()