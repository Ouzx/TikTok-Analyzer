import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import logger.main as logger
import scraper.strings as stri
import db.main as DB


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome(
            stri.driver_path, options=self.get_options())

        self.post_count = 0
        self.link = Scraper.get_base_link()

        self.page_data = {}
        self.posts_data = []
        self.posts_activity = []

        self.driver.get(self.link)
        self.scrape()
        self.driver.close()

    def scrape(self):
        self.scroll_end_of_page()

        self.page_data = self.get_page_data()
        posts = self.get_posts()

        posts = reversed(posts)

        for post in posts:
            self.posts_data.append(self.get_post_data(post))

        for post_data in self.posts_data:
            self.driver.get(post_data['link'])
            post_data.update(self.get_inner_post_data(post_data))

        self.SaveData()

    def get_page_data(self):
        page_data = stri.page_template.copy()
        page_data['name'] = self.driver.find_element(
            By.CSS_SELECTOR, stri.selectors["acc"]).text
        page_data["following"] = self.driver.find_element(
            By.CSS_SELECTOR, stri.selectors["acc_following"]).text
        page_data["followers"] = self.driver.find_element(
            By.CSS_SELECTOR, stri.selectors["acc_followers"]).text
        page_data['likes'] = self.driver.find_element(
            By.CSS_SELECTOR, stri.selectors["acc_likes"]).text
        page_data['bio'] = self.driver.find_element(
            By.CSS_SELECTOR, stri.selectors["acc_bio"]).text

        logger.Log(f"Page data: {page_data}")

        return page_data

    def get_posts(self):
        posts = self.driver.find_elements(
            By.CSS_SELECTOR, stri.selectors["post"])
        self.post_count = len(posts)
        logger.Log(f"Found {len(posts)} posts")
        return posts

    def get_post_data(self, post):
        post_data = stri.post_template.copy()
        post_data['view'] = post.find_element(
            By.CSS_SELECTOR, stri.selectors["post_view"]).text
        post_data['name'] = post.find_element(
            By.CSS_SELECTOR, stri.selectors["post_name"]).get_attribute('alt')
        post_data['link'] = post.find_element(
            By.CSS_SELECTOR, stri.selectors["post_link"]).get_attribute("href")

        logger.Log(f"Post outer data: {post_data}")
        return post_data

    def get_inner_post_data(self, post_data):
        post_data['like'] = self.driver.find_element(
            By.CSS_SELECTOR, stri.selectors["post_like"]).text
        post_data['comment'] = self.driver.find_element(
            By.CSS_SELECTOR, stri.selectors["post_comment"]).text
        logger.Log(f"Total post data: {post_data}")
        return post_data

    def SaveData(self):
        _page_data = {
            "name": self.page_data["name"],
            "following": self.page_data["following"],
            "followers": self.page_data["followers"],
            "likes": self.page_data["likes"],
            "bio": self.page_data["bio"],
            "post_count": self.post_count,
            "link": self.link
        }
        DB.create_page(_page_data)

        for post_data in self.posts_data:
            _post_data = {
                "page_link": self.link,
                "link": post_data["link"],
                "name": post_data["name"],
            }

            _post_activity = {
                "post_link": post_data["link"],
                "like": post_data["like"],
                "comment": post_data["comment"],
                "view": post_data["view"]
            }

            DB.create_post(_post_data)
            DB.create_post_activity(_post_activity)

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

    @ staticmethod
    def get_base_link():
        with open(stri.link_path, "r") as f:
            return f.read()

    @ staticmethod
    def get_options():
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return options
