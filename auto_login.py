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
    browser.add_cookie({"name": "MUSIC_U", "value": "00553AAF05C98C43E8D1AD38FA57990D5B8B5834B095DC2EA85DCFDF58127D1B4D9E69E3BA996C58B45332D043AB8D4CC06CECBB576D9AF58FAE5F0284CC52DD8E1BFF2225E6ECC991B6C14CB4629D5DD049BE308182FC1F84780AEF7CD928CF9576FDA2F5DADC5ECE5210021086998EA4C0DF725F0A3CDD194532C2F79E1CF5C49C089800E6B38E5C5F06D219B055C448988B383819DB4A1BE83276D3CA2F037A3E1BC0980170FCB8CE824904A897E3321940DBBE38FE39E837B8043A22AFC5BB92F43FD3370C6D444D6D892014D5F4B8572FA87D563642A6B6F969F1B228190F67EE7138D74825DDF794C1A888B60E7F72FBF35CD1C4EC0928F45F98829872477C59851E17F60B8FCCA9630732710F27ADFB1C8C4AF5EEB2FD83BA376325FF1024B1FD7639351B6A4C41BC85039D591F031908059046413C08B4D71F9CE819E3385AC0AFE0FACD0A9921787E8872C59667A49F5880549911C8ECE6BD6A476921"})
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
