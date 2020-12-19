from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from bs4 import BeautifulSoup
import warnings
import json
import config
import db
import logging
import logger
import weather_api


def scrape_data(username, password, keyword, limit=1000):
    # Setting the driver and opening Instagram
    driver = webdriver.Chrome()
    driver.get(config.BASE_URL)
    # Login in, filling search boxes, etc
    fill_login(driver, username, password)
    fill_keyword(driver, keyword)

    driver_json = webdriver.Chrome()
    driver_json.get(config.BASE_URL)
    # Login in, filling search boxes, etc
    fill_login(driver_json, username, password)

    # Do the real scraping
    save_content(driver, driver_json, limit, keyword)


def fill_login(driver, username, password):
    # Finding the auth boxes by CSS Selectors
    username_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, config.AUTH_USER_SEL)))
    password_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, config.AUTH_PASS_SEL)))

    # Typing in the auth values provided
    username_box.clear()
    password_box.clear()
    username_box.send_keys(username)
    password_box.send_keys(password)

    # Finding the login button by CSS Selector and clicking on it
    login_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, config.SUBMIT_SELECTOR)))
    login_btn.click()

    # Finding the "not now" buttons by XPATH and clicking on them
    not_now_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config.NOT_NOW_XPATH)))
    not_now_btn.click()
    not_now_btn2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config.NOT_NOW_XPATH)))
    not_now_btn2.click()


def fill_keyword(driver, keyword):
    # If no user searched without # or @, we add a #
    keyword = "#" + keyword if keyword[0] not in ["@", "#"] else keyword

    # Finding the search box by XPATH and typing in the keyword
    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config.SEARCH_XPATH)))
    search_box.clear()
    search_box.send_keys(keyword)

    # For finding the right keyword in the list
    keyword = keyword[1:] if keyword[0] == "@" else keyword

    # Finding the hashtag button by XPATH and clicking on it
    hashtag_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config.hash_xpath(keyword))))
    hashtag_btn.click()


def save_content(driver, driver_json, limit, keyword):
    # Ignoring warnings from Beautiful Soup (not relevant for this project)
    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

    # There are different selectors for User page and in Hashtag page
    post_selector = config.POST_SELECTOR_BY_USER if keyword[0] == "@" else config.POST_SELECTOR_BY_HASH

    # We find the first of the page and we click on it
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
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, config.LIKES_SELECTOR)))
            spans = BeautifulSoup(likes_element.get_attribute("innerHTML"), "html.parser").find_all("span")

            # Fixing instagram specific issue when scraping likes
            if len(spans) == 0:
                likes = 0
            elif spans[-1].text == "1 view":
                likes = 1
            else:
                likes = int(spans[-1].text.replace(",", ""))

            # We scrape the hashtags
            hash_element = WebDriverWait(driver, 10) \
                .until(EC.presence_of_element_located((By.CSS_SELECTOR, config.HASH_SELECTOR)))
            anchors = BeautifulSoup(hash_element.get_attribute("innerHTML"), "html.parser").find_all("a")
            hash_links = [anchor.get("href") for anchor in anchors if "/explore/tags/" in anchor.get("href")]
            hashtags = [hash_link.split("/")[-2] for hash_link in hash_links]

            # We scrape the location
            try:
                location_element = WebDriverWait(driver, 10) \
                    .until(EC.presence_of_element_located((By.CSS_SELECTOR, config.LOCATION_SELECTOR)))
                location = location_element.find_element_by_class_name("O4GlU").text
            except selenium.common.exceptions.NoSuchElementException:
                location = None

        except selenium.common.exceptions.TimeoutException:
            logger.log(logging.INFO, msg="Post took too long - SKIPPING")
        else:
            # We go save the user info (followers, following, etc)
            user_id = save_user(driver_json, username)
            # We go save the post info (likes, views, timestamp, etc)
            post_id = save_post(driver_json, user_id, link, likes, location)
            # We save the hashtags
            for hashtag in hashtags:
                hashtag_id = db.add_hashtag(hashtag)
                db.add_post_hashtag(post_id, hashtag_id)
        finally:
            # We find the arrow for the next post and we click on it
            next_post = WebDriverWait(driver, 10) \
                .until(EC.presence_of_element_located((By.CLASS_NAME, config.NEXT_POST_CLASS)))
            next_post.click()


def save_user(driver_json, username):
    try:
        driver_json.get(f"{config.BASE_URL}{username}/{config.DATA_TO_JSON}")
        data = json.loads(BeautifulSoup(driver_json.page_source, 'html.parser').find('body').get_text())
        full_user = data["graphql"]["user"]
        user = {
            "username": username,
            "full_name": full_user["full_name"],
            "posts": full_user["edge_owner_to_timeline_media"]["count"],
            "igtv_posts": full_user["edge_felix_video_timeline"]["count"],
            "followers": int(full_user["edge_followed_by"]["count"]),
            "following": int(full_user["edge_follow"]["count"]),
            "bio": full_user["biography"],
            "external_url": full_user["external_url"],
            "is_private": full_user["is_private"],
            "is_verified": full_user["is_verified"],
            "is_business_account": full_user["is_business_account"],
            "business_category_name": full_user["business_category_name"],
            "is_joined_recently": full_user["is_joined_recently"]
        }
        return db.add_user(user)
    except json.decoder.JSONDecodeError as ex:
        print(ex)
        return db.add_simple_user(username)


def save_post(driver_json, user_id, link, likes, location):
    try:
        driver_json.get(f"{link}{config.DATA_TO_JSON}")
        data = json.loads(BeautifulSoup(driver_json.page_source, 'html.parser').find('body').get_text())
        full_post = data["graphql"]["shortcode_media"]
        post = {
            "user_id": user_id,
            "link": link,
            "caption": full_post["edge_media_to_caption"]["edges"][-1]["node"]["text"][:255],
            "likes": full_post["edge_media_preview_like"]["count"],
            "comments": full_post["edge_media_to_parent_comment"]["count"],
            "is_video": full_post["is_video"],
            "views": full_post["video_view_count"] if "video_view_count" in full_post else None,
            "temperature": None,
            "weather": None,
            "timestamp": full_post["taken_at_timestamp"]
        }

        # if there is a location let's add it
        full_location = full_post["location"]
        location_id = None
        if full_location:
            address = json.loads(full_location["address_json"]) if full_location["address_json"] else None
            location = {
                "name": full_location["name"],
                "slug": full_location["slug"],
                "country": address["country_code"] if address else None,
                "city": address["city_name"] if address and len(address["city_name"]) > 0 else None
            }
            # Getting Geo location from google API
            geo_address = f"{location['city']}, {location['country']}"
            lat, lon = weather_api.google_geo(geo_address)
            location["latitude"] = lat
            location["longitude"] = lon
            # Getting weather from open weather API
            temperature, weather = weather_api.get_weather(lat, lon, post["timestamp"])
            post["temperature"] = temperature
            post["weather"] = weather

            location_id = db.add_location(location)

        # We save the post
        post_id = db.add_post(user_id, post)

        # If there is a location we save the aux table entry
        if location_id:
            db.add_post_location(post_id, location_id)

        return post_id
    except json.decoder.JSONDecodeError as ex:
        print(ex)
        post_id = db.add_simple_post(user_id, link, likes)
        if location:
            location_id = db.add_simple_location(location)
            db.add_post_location(post_id, location_id)
        return post_id
