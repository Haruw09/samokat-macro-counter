from samokat_kbju.cart.parser import (
    create_driver,
    extract_cart_items,
    open_samokat,
    wait_for_page_ready,
)


def main() -> None:
    driver = create_driver()

    try:
        open_samokat(driver)
        wait_for_page_ready(driver)

        input("Открой корзину вручную, потом нажми Enter...")

        items = extract_cart_items(driver)

        if not items:
            print("Товары корзины не найдены.")
        else:
            for index, item in enumerate(items, start=1):
                print(f"{index}. {item.name}")
                print(f"   quantity: {item.quantity}")
                print(f"   packaging: {item.raw_packaging}")
                print(f"   current price: {item.price_current}")
                print(f"   old price: {item.price_old}")
                print()

        input("Press Enter to close...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()