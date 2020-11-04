import requests
from bs4 import BeautifulSoup
import argparse
import getpass
import sys
import time
import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.keys import Keys


def scrape_insta(username, password, keyword, limit=50):
    # Setting the driver and opening Instagram
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/")

    # Finding the auth boxes by CSS Selectors
    username_box = WebDriverWait(driver, 10)\
        .until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_box = WebDriverWait(driver, 10)\
        .until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    # Typing in the auth values provided
    username_box.clear()
    password_box.clear()
    username_box.send_keys(username)
    password_box.send_keys(password)

    # Finding the login button by CSS Selector and clicking on it
    login_btn = WebDriverWait(driver, 10)\
        .until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_btn.click()

    # Finding the "not now" buttons by XPATH and clicking on them
    not_now_btn = WebDriverWait(driver, 10)\
        .until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
    not_now_btn.click()
    not_now_btn2 = WebDriverWait(driver, 10)\
        .until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
    not_now_btn2.click()

    # Finding the search box by XPATH and typing in the keyword
    search_box = WebDriverWait(driver, 10)\
        .until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    search_box.clear()
    search_box.send_keys(keyword)

    # Finding the hashtag button by XPATH and clicking on it
    hashtag_btn = WebDriverWait(driver, 10)\
        .until(expected_conditions.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{keyword}')]")))
    hashtag_btn.click()

    # Do the real scraping
    print_content(driver, limit)


def print_content(driver, limit):
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

                    # We save the post in the dictionary for reference
                    posts[post_id] = post_counter
                    # We print all the data
                    print(f"POST {post_counter}")
                    print(f"Link: {link}")
                    print(f"Username: {match.group(3)}")
                    print(f"{match.group(1)} likes")
                    print(f"{match.group(2)} comments")

                    # We get all the hashtags and print them
                    hashtag_items = soup.find_all("meta", {"property": "instapp:hashtags"})
                    hashtags = [hashtag_item["content"] for hashtag_item in hashtag_items]
                    print(f"Hashtags: {hashtags}")

                    post_counter += 1
                    if post_counter > limit:
                        print("Limit reached")
                        break

        # Scrolling to the end of page for loading more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def get_auth_by_file(filename):
    with open(filename, "r") as file:
        username = file.readline()
        password = file.readline()
    return username, password

def get_auth_by_console():
    username = input('Username: ')
    password = getpass.getpass(prompt="Password: ", stream=None)
    return username, password

def args_credentials():
    parser = argparse.ArgumentParser(description="scrape instagram by keyword (hashtag)")
    parser.add_argument("-c", "--console", help="option for logging in through the console", action="store_true"),
    parser.add_argument("-f", "--filename", help="option for logging in through a file\n"
                                                 "username must be in the first line and password in the second one"),
    parser.add_argument("key_type", help="which type page to look for", choices=["user", "hashtag"]),
    parser.add_argument("keyword", help="the keyword to find in instagram"),
    args = parser.parse_args()

    username, password = "", ""
    if args.console:
        username, password = get_auth_by_console()
    elif args.filename:
        try:
            username, password = get_auth_by_file(args.filename)
        except FileNotFoundError:
            print("The provided file does not exist")
    return username, password

def console_credentials():
    print('Welcome to Insta Scrapper developed by Yaniv Goldfrid and Dana Velibekov.')
    while True:
        try:
            choice = ''
            username = ''
            password = ''
            while True:
                choice = input('What is your preferred method of authentication? [f]ile/[c]onsole: ')
                if choice in ['f', 'c']:
                    break
                else:
                    print("Invalid option")

            if choice == 'f': # file credentials
                while True:
                    file_path = input('Path to file containing auth details: ')
                    try:
                        username, password = get_auth_by_file(file_path)
                        print(file_path)
                        break
                    except FileNotFoundError:
                        print(f"Not found file at path: {file_path}")
                pass
            else: # file credentials
                username, password = get_auth_by_console()
                break

            keyword = input(f'Search: (add "#" in-front to look for hashtags): ')
            return username, password, keyword

        except KeyboardInterrupt:
            print("\nSee ya!")
            sys.exit(0)

def main():

    # main call to function
    username, password, keyword = console_credentials()
    scrape_insta(username=username,
                 password=password,
                 keyword=keyword,
                 limit=1000)


if __name__ == "__main__":
    main()
