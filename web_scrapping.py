import logging
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DOWNLOAD_DIR = "/home/timur/Downloads/HSE_SMADIMO_GP2/scrapping_json_data"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DIR,  # Папка загрузки
    "download.prompt_for_download": False,  # Отключает всплывающее окно
    "download.directory_upgrade": True,  # Разрешает смену папки загрузки
    "safebrowsing.enabled": True  # Отключает предупреждения безопасности
})

driver = webdriver.Chrome(options=options)

logging.info(f"Загруженные файлы будут сохраняться в: {DOWNLOAD_DIR}")


def close_cookie_banner():
    """Закрываем баннер с куками, если он появляется."""
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Принять')] | //button[contains(text(),'Принять все')]")
            )
        )
        cookie_button.click()
        # time.sleep(1)
    except Exception:
        pass


def click_element(xpath, timeout=15, scroll=True):
    """
    Ждёт, пока элемент по заданному XPATH станет кликабельным, скроллит его и кликает.
    """
    elem = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    if scroll:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.5)
    elem.click()
    time.sleep(1)


def get_data_from_chart(url, json_name):
    """
    1. Открывает страницу с графиком.
    2. Закрывает cookie-баннер.
    3. Нажимает на кнопку с периодом «3г».
    4. Затем нажимает на кнопку «Скачать JSON».
    """
    driver.get(url)
    close_cookie_banner()

    time.sleep(5)
    # Нажимаем на кнопку "3г"
    period_xpath = "//*[contains(text(), '3г') or contains(text(), '3 г') or contains(text(), '3 года')]"
    click_element(period_xpath, timeout=30, scroll=False)

    time.sleep(5)
    # Нажимаем на кнопку "Скачать JSON"
    download_json_xpath = "//*[contains(text(), 'Скачать JSON')]"
    click_element(download_json_xpath, timeout=30, scroll=False)

    time.sleep(5)
    # Ждём, пока JSON-файл появится в папке загрузки
    json_path = os.path.join(DOWNLOAD_DIR, f"{json_name}.json")
    logging.info(f"JSON загружен и сохранён в '{json_path}'")


try:
    get_data_from_chart("https://www.blockchain.com/ru/explorer/charts/trade-volume", "trade-volume")
    get_data_from_chart("https://www.blockchain.com/explorer/charts/n-transactions-per-block", "n-transactions-per-block")
    get_data_from_chart("https://www.blockchain.com/explorer/charts/n-payments-per-block", "n-payments-per-block")
    get_data_from_chart("https://www.blockchain.com/ru/explorer/charts/hash-rate", "hash-rate")
    get_data_from_chart("https://www.blockchain.com/ru/explorer/charts/fees-usd-per-transaction", "fees-usd-per-transaction")
    get_data_from_chart("https://www.blockchain.com/ru/explorer/charts/cost-per-transaction", "cost-per-transaction")
    get_data_from_chart("https://www.blockchain.com/ru/explorer/charts/n-unique-addresses", "n-unique-addresses")
    get_data_from_chart("https://www.blockchain.com/ru/explorer/charts/mvrv", "mvrv")
    get_data_from_chart("https://www.blockchain.com/ru/explorer/charts/nvt", "nvt")
    get_data_from_chart("https://www.blockchain.com/ru/explorer/charts/nvts", "nvts")

finally:
    driver.quit()
