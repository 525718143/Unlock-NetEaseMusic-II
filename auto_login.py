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
    browser.add_cookie({"name": "MUSIC_U", "value": "008B3DDB57A798E5917C076F7B3B3488B1CF902678BDDD5ED95B67AF8C41853DC637E4E419AB1E57CE45B454D3C74CF3325AB852DC64162E5C50BC9A1543FB3E754822B728EE82F2CDB810907A12610D51360FD4BC3732C651BE6C58BA2E2FF5C6662E4743C24EF3BD302A6D5C36FF8A3E86D2DCC08B9B0DFCFEFF3B823201A6530E9E823B9EC5C3D61B81AABD9719417CCC11FF8A012EA91B75D0CC80B959F53E86D0D1DC4A1D36D06078C4EE865645CC3D6084677BE8F59846E458CA5179A35E03B15634E944DBDF706B199AA35019CCB106DFAF33F0D9DA1E69213B01A743C445A7DD02A8D47E386B3882A3D446CBF599640E0609A78061ABD9C424BAA7C10365C03BAF77E83335FAFFE3F420EA9578841EE51BD8522C3426D98BE79FF16CCA8536831CC2A38E7B6A5F893D8F917E994F82871AA666E176814533496FE8C46D779D22C7E2506565F25F0DC52994C245B42A1C83ECB4AEE39F9717AC79E34F85"})
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
