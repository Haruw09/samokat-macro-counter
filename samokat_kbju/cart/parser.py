import re
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from samokat_kbju.cart.models import CartItem


def create_driver() -> webdriver.Firefox:
    options = Options()
    options.add_argument("--width=1440")
    options.add_argument("--height=1000")

    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    return driver


def open_samokat(driver: webdriver.Firefox) -> None:
    driver.get("https://samokat.ru")


def wait_for_page_ready(driver: webdriver.Firefox, timeout: int = 15) -> None:
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def clean_text(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split()).strip()


def parse_price(text: str) -> Optional[float]:
    cleaned = clean_text(text).replace("₽", "").replace(" ", "")
    match = re.search(r"\d+[.,]?\d*", cleaned)
    if not match:
        return None
    return float(match.group(0).replace(",", "."))


def parse_quantity(text: str) -> Optional[int]:
    cleaned = clean_text(text)
    return int(cleaned) if cleaned.isdigit() else None


def safe_find_text(parent: WebElement, by: By, selector: str) -> Optional[str]:
    elements = parent.find_elements(by, selector)
    for element in elements:
        text = clean_text(element.text)
        if text:
            return text
    return None


def safe_find_all_texts(parent: WebElement, by: By, selector: str) -> list[str]:
    texts = []
    for element in parent.find_elements(by, selector):
        text = clean_text(element.text)
        if text:
            texts.append(text)
    return texts


def find_cart_item_cards(driver: webdriver.Firefox) -> list[WebElement]:
    return driver.find_elements(By.CSS_SELECTOR, "div[class^='ProductItem_root__']")


def extract_cart_item(card: WebElement) -> Optional[CartItem]:
    name = safe_find_text(card, By.CSS_SELECTOR, "span[class*='ProductItem_name__']")
    if not name:
        return None

    raw_packaging = safe_find_text(
        card,
        By.CSS_SELECTOR,
        "span[class*='ProductItem_specification__']",
    )

    quantity = None
    action_texts = safe_find_all_texts(
        card,
        By.CSS_SELECTOR,
        "div[class*='CartItemActions_root__'] span",
    )
    for text in action_texts:
        parsed_qty = parse_quantity(text)
        if parsed_qty is not None:
            quantity = parsed_qty
            break

    price_current = None
    price_old = None
    price_texts = safe_find_all_texts(
        card,
        By.CSS_SELECTOR,
        "div[class*='ItemPrice_root__'] span",
    )

    parsed_prices = []
    for text in price_texts:
        price = parse_price(text)
        if price is not None:
            parsed_prices.append(price)

    if len(parsed_prices) == 1:
        price_current = parsed_prices[0]
    elif len(parsed_prices) >= 2:
        price_old = parsed_prices[0]
        price_current = parsed_prices[-1]

    return CartItem(
        name=name,
        quantity=quantity or 1,
        price_current=price_current,
        price_old=price_old,
        raw_packaging=raw_packaging,
    )


def extract_cart_items(driver: webdriver.Firefox) -> list[CartItem]:
    cards = find_cart_item_cards(driver)
    items: list[CartItem] = []

    for card in cards:
        item = extract_cart_item(card)
        if item is not None:
            items.append(item)

    return items