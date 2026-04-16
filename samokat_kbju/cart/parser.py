from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def create_driver() -> webdriver.Firefox:
    options = Options()
    options.add_argument("--width=1440")
    options.add_argument("--height=1000")

    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    return driver


def open_samokat_cart(driver: webdriver.Firefox) -> None:
    driver.get("https://samokat.ru")