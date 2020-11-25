import requests
from bs4 import BeautifulSoup
import time
import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import db
import warnings
import config


def scrape_data(username, password, keyword, limit=50):
    # Setting the driver and opening Instagram
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/")

    # Login in, filling search boxes, etc
    fill_info(driver, username, password, keyword)

    # Do the real scraping
    save_content(driver, limit, keyword)


def fill_info(driver, username, password, keyword):
    # Finding the auth boxes by CSS Selectors
    username_box = WebDriverWait(driver, 10) \
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_box = WebDriverWait(driver, 10) \
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    # Typing in the auth values provided
    username_box.clear()
    password_box.clear()
    username_box.send_keys(username)
    password_box.send_keys(password)

    # Finding the login button by CSS Selector and clicking on it
    login_btn = WebDriverWait(driver, 10) \
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_btn.click()

    # Finding the "not now" buttons by XPATH and clicking on them
    not_now_btn = WebDriverWait(driver, 10) \
        .until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
    not_now_btn.click()
    not_now_btn2 = WebDriverWait(driver, 10) \
        .until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
    not_now_btn2.click()

    keyword = "#" + keyword if keyword[0] not in ["@", "#"] else keyword

    # Finding the search box by XPATH and typing in the keyword
    search_box = WebDriverWait(driver, 10) \
        .until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    search_box.clear()
    search_box.send_keys(keyword)

    keyword = keyword[1:] if keyword[0] == "@" else keyword

    # Finding the hashtag button by XPATH and clicking on it
    hashtag_btn = WebDriverWait(driver, 10) \
        .until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{keyword}')]")))
    hashtag_btn.click()


def save_content(driver, limit, keyword):
    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

    post_selector = config.POST_SELECTOR_BY_USER if keyword[0] == "@" else config.POST_SELECTOR_BY_HASH

    first_post = WebDriverWait(driver, 10) \
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, post_selector)))
    first_post.click()

    for _ in range(limit):
        try:
            # We scrape the username
            user_element = WebDriverWait(driver, 10)\
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, config.USER_SELECTOR)))
            username = BeautifulSoup(user_element.get_attribute("innerHTML"), "html.parser").text

            # We scrape the link
            link_element = WebDriverWait(driver, 10)\
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, config.LINK_SELECTOR)))
            link = BeautifulSoup(link_element.get_attribute("href"), "html.parser").text

            # We scrape the likes
            likes_element = WebDriverWait(driver, 10)\
                .until(EC.presence_of_element_located((By.CSS_SELECTOR,config.LIKES_SELECTOR)))
            spans = BeautifulSoup(likes_element.get_attribute("innerHTML"), "html.parser").find_all("span")

            # Fixing instagram specific issue when scraping likes
            if len(spans) == 0:
                likes = 0
            elif spans[-1].text == "1 view":
                likes = 1
            else:
                likes = spans[-1].text

            # We scrape the hashtags
            hash_element = WebDriverWait(driver, 10) \
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, config.HASH_SELECTOR)))
            anchors = BeautifulSoup(hash_element.get_attribute("innerHTML"), "html.parser").find_all("a")
            hash_links = [anchor.get("href") for anchor in anchors if "/explore/tags/" in anchor.get("href")]
            hashtags = [hash_link.split("/")[-2] for hash_link in hash_links]
        except Exception:
            print("Post took too long - SKIPPING")
        else:
            # We save the user, post and hashtags in the db
            user_id = db.add_simple_user(username)
            post_id = db.add_post(user_id, link, likes)
            for hashtag in hashtags:
                hashtag_id = db.add_hashtag(hashtag)
                db.add_post_hashtag(post_id, hashtag_id)
        finally:
            next_post = WebDriverWait(driver, 10) \
                .until(EC.presence_of_element_located((By.CLASS_NAME, "coreSpriteRightPaginationArrow")))
            next_post.click()
