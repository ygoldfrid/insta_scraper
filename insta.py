from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import argparse
import time


def scrape_insta(username, password, keyword):
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
    keyword = "#" + keyword
    search_box.send_keys(keyword)

    # Finding the hashtag button by XPATH and clicking on it
    hashtag_btn = WebDriverWait(driver, 10)\
        .until(expected_conditions.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{keyword}')]")))
    hashtag_btn.click()

    # Waiting for page to load
    time.sleep(5)

    # Scrolling down the page to load more images
    driver.execute_script("window.scrollTo(0, 4000);")

    # Finding all images in the page by the tag name img
    images = driver.find_elements_by_tag_name("img")

    for image in images:
        print(image.get_attribute("alt"))
        print(image.get_attribute("src"))


def get_auth_by_file(filename):
    with open(filename, "r") as file:
        username = file.readline()
        password = file.readline()
    return username, password


def get_auth_by_console():

    """TODO: Auth through command line"""

    print("Logging in from console")
    return "", ""


def main():

    """TODO: Develop so that -c or -f are at least one required but not both. Keyword must always be required"""

    parser = argparse.ArgumentParser(description="scrape instagram by keyword (hashtag)")
    parser.add_argument("-c", "--console", help="option for logging in through the console", action="store_true"),
    parser.add_argument("-f", "--filename", help="option for logging in through a file\n"
                                                 "username must be in the first line and password in the second one"),
    parser.add_argument("keyword", help="the keyword (hashtag) to find in instagram"),
    args = parser.parse_args()

    username, password = "", ""
    if args.console:
        username, password = get_auth_by_console()
    elif args.filename:
        try:
            username, password = get_auth_by_file(args.filename)
        except FileNotFoundError:
            print("The provided file does not exist")

    scrape_insta(username, password, args.keyword)


if __name__ == "__main__":
    main()
