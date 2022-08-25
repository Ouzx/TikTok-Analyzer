import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import logger.main as logger
import scraper.strings as str


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome(str.driver_path)
        self.scrape()

    def scrape(self):
        self.driver.get(Scraper.get_base_link())
        self.scroll_end_of_page()

    def scroll_end_of_page(self):
        logger.Log("Scrolling to the end of the page")
        pre_scroll_height = self.driver.execute_script(
            'return document.body.scrollHeight;')
        while True:
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(5)
            post_scroll_height = self.driver.execute_script(
                'return document.body.scrollHeight;')

            if pre_scroll_height == post_scroll_height:
                break
            pre_scroll_height = post_scroll_height

    @staticmethod
    def get_base_link():
        with open(str.link_path, "r") as f:
            return f.read()
