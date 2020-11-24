import requests
from bs4 import BeautifulSoup
import time
import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import db


def scrape_data(username, password, keyword, limit=50):
    # Setting the driver and opening Instagram
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/")

    # Finding the auth boxes by CSS Selectors
    username_box = WebDriverWait(driver, 10) \
        .until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_box = WebDriverWait(driver, 10) \
        .until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    # Typing in the auth values provided
    username_box.clear()
    password_box.clear()
    username_box.send_keys(username)
    password_box.send_keys(password)

    # Finding the login button by CSS Selector and clicking on it
    login_btn = WebDriverWait(driver, 10) \
        .until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_btn.click()

    # Finding the "not now" buttons by XPATH and clicking on them
    not_now_btn = WebDriverWait(driver, 10) \
        .until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
    not_now_btn.click()
    not_now_btn2 = WebDriverWait(driver, 10) \
        .until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
    not_now_btn2.click()

    keyword = "#" + keyword if keyword[0] not in ["@", "#"] else keyword

    # Finding the search box by XPATH and typing in the keyword
    search_box = WebDriverWait(driver, 10) \
        .until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    search_box.clear()
    search_box.send_keys(keyword)

    keyword = keyword[1:] if keyword[0] == "@" else keyword

    # Finding the hashtag button by XPATH and clicking on it
    hashtag_btn = WebDriverWait(driver, 10) \
        .until(expected_conditions.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{keyword}')]")))
    hashtag_btn.click()

    # Do the real scraping
    save_content(driver, limit)


def save_content(driver, limit):
    # Dictionary to store all posts uniquely
    posts = {}
    post_counter = 1
    while post_counter <= limit:
        # Waiting for page to load
        time.sleep(3)
        # Finding all hyperlinks in the page by the tag name 'a'
        hyperlinks = driver.find_elements_by_tag_name("a")
        for hyperlink in hyperlinks:
            link = hyperlink.get_attribute("href")
            # We only care about the /p/ links which means posts
            if "/p/" in link:
                # We slice the link to get a unique identifier
                post_id = link[28:-1]
                if post_id not in posts:
                    print("####################################################")
                    # Now we are ready to go to each link and get the data from it
                    response = requests.get(link)
                    soup = BeautifulSoup(response.content, "html.parser")

                    # We look for the tag meta with the description name. If it doesn't exist we skip the post
                    description = soup.find("meta", {"name": "description"})
                    if not description:
                        print("No description - Skipping")
                        continue

                    # We get the content from the html and we do a regex search to get the desired data
                    content = description["content"]
                    match = re.search(r"([\dkm.,]+)\sLikes,\s([\dkm.,]+)\sComments\s-\s[^@]*(@[\w.-]+)", content)

                    # If there is no regex match it means there is not enough info in the post, so we skip it
                    if not match:
                        print("No match - Skipping")
                        continue

                    likes = match.group(1)
                    comments = match.group(2)
                    username = match.group(3)

                    # We save the post in the dictionary for reference
                    posts[post_id] = post_counter

                    # We print all the data
                    print(f"POST {post_counter}")
                    print(f"Link: {link}")
                    print(f"Username: {username}")
                    print(f"{likes} likes")
                    print(f"{comments} comments")

                    # We get all the hashtags and print them
                    hashtag_items = soup.find_all("meta", {"property": "instapp:hashtags"})
                    hashtags = [hashtag_item["content"] for hashtag_item in hashtag_items]
                    print(f"Hashtags: {hashtags}")

                    # We save the user, post and hashtags in the db
                    user_id = db.add_simple_user(username)
                    db.add_post(user_id, link, likes, comments)
                    for hashtag in hashtag:
                        db.add_hashtag(hashtag)

                    post_counter += 1
                    if post_counter > limit:
                        print("Limit reached")
                        break

        # Scrolling to the end of page for loading more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
