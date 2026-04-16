from samokat_kbju.cart.parser import create_driver, open_samokat_cart


def main() -> None:
    driver = create_driver()

    try:
        open_samokat_cart(driver)
        input("Press Enter to close...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()