from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


def whatsapp_initializer(driver_address: str):
    # Adding Arguments to chrome browser so that it wont Crash
    options = Options();
    options.add_argument('--user-data-dir=./User_Data')
    options.add_argument("start-maximized");
    options.add_argument("disable-infobars");
    options.add_argument("--disable-extensions");
    options.add_argument("--disable-gpu");
    options.add_argument("--disable-dev-shm-usage");
    options.add_argument("--no-sandbox");

    driver = webdriver.Chrome("{0}".format(driver_address), options=options)

    # Open Website
    driver.get('https://web.whatsapp.com/')
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/header/div[2]/div/span/div[3]/div/span'))
        WebDriverWait(driver, 180).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        pass

    return driver


def whatsapp_closer(driver: webdriver):
    driver.close()