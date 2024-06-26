from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import CHROME_WEB_DRIVER_PATH


def initialize_web_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(
        executable_path=CHROME_WEB_DRIVER_PATH, options=chrome_options)
    return driver
