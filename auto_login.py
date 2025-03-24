# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00B0027A9573D819873B4147272BA7AA66ED22D26D7331789F08A5558CF32E77127ECB3661A279A509C270BFC278920B36159CDB3CD809123DC2AB0493BC55F8A04B56F6F63C48677C6591D6C3CCAC39AC63BAEF4F153D3421F0FFAE0F655F19E377CFE5115E78C60AB2E5FAD892705267398D86479EE987AB6B13F1CEBE7016F1CD3256DF5651CBDDA27E8E510EEE10DBAEAF8356C980F840B6987406EC973F640ACBD0FE48F46372F3F4BCCD0891A7D3CB96045F696CAB0A91AF7EC329946E98DFAA1D397E022FEE02FFF47235F6C69572854081DA39294232C243B52C7B1252AD0B2621A31D56A3B3D9DAAA9D3F7990F1CB39CCF227AA19D5546B233C82AE891534AD48408E341CCFE8BF9297531F9E46EBFA1249F3B0295B9C5BC4D84CF0EDEA94A821959C5217668340185CA2E5E35CCDAA600C91644D9C864B340DFAA3C719E085BF5546291185A534689B9A89A1572B5A20981EB240473DC92B6DC1A904"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
