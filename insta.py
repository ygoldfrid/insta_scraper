import argparse
import sys
from scraper import scrape_data
import db
import logger
import logging
import config


def get_auth_by_file(filename):
    with open(filename, "r") as file:
        username = file.readline().strip()
        password = file.readline().strip()
    return username, password


def get_auth_by_console():
    username = input('Username: ')
    password = input('Password: ')
    return username, password


def interactive_credentials():
    print('\nWelcome to Insta Scrapper developed by Yaniv Goldfrid and Dana Velibekov')
    try:
        choice = ''
        while choice.lower() not in ['f', 'c']:
            choice = input('Please select preferred method of authentication:\n[f]ile (default)\n[c]onsole\n')
            choice = "f" if choice == "" else choice
            if choice.lower() not in ['f', 'c']:
                print("Invalid option")
                logger.log(logging.INFO,
                           msg=f"User failed to chose between file and console interaction", destination=logger.FILE)

        username, password = '', ''
        if choice.lower() == 'f':  # file credentials
            while len(username) == 0 and len(password) == 0:
                file_path = input('Please type in the path to your auth (default auth.txt)\n')
                file_path = "auth.txt" if file_path == "" else file_path
                try:
                    username, password = get_auth_by_file(file_path)
                    print("You selected: " + file_path)
                except FileNotFoundError:
                    print(f"Not found file at path: {file_path}")
                    logger.log(logging.ERROR,
                               msg=f"Not found file at path: {file_path}", destination=logger.FILE)
        else:  # console credentials
            username, password = get_auth_by_console()

        keyword = ''
        while len(keyword) == 0:
            keyword = input(
                f'Please type in your search keyword as you would do on Instagram (#cats, @beyonce, etc):\n')
            if keyword == '':
                print("Please type a search keyword!")
                logger.log(logging.INFO,
                           msg='User left the "keyword" blank', destination=logger.FILE)

        return username, password, keyword

    except KeyboardInterrupt:
        print("\nSee ya!")
        logger.log(logging.INFO, msg='User ended the program (KeyboardInterrupt exception)', destination=logger.FILE)
        sys.exit(0)


def main():
    logger.configure()
    logger.log(logging.INFO,
               msg="User started interacting with the scraper", destination=logger.FILE)

    parser = argparse.ArgumentParser(description="scrape instagram by keyword (hashtag)")
    # used only within cli mode
    parser.add_argument("-k", "--keyword", help="the keyword to find in instagram (by hashtag or username)")
    parser.add_argument("-l", "--limit", default=1000, help="limit of instagram posts to scrap")
    parser.add_argument("-f", "--filename", help="option for logging in through a file\n"
                                                 "username must be in the first line and password in the second one")
    args = parser.parse_args()

    username, password, keyword = "", "", ""

    # cli mode
    if args.keyword:
        keyword = args.keyword
        filename = args.filename if args.filename else "auth.txt"

        try:
            username, password = get_auth_by_file(filename)

        except FileNotFoundError:
            logger.log(logging.ERROR,
                       msg="Neither the credentials file were provided nor the default auth.txt were found")
            quit(0)

    # interactive mode (default)
    else:
        username, password, keyword = interactive_credentials()

    try:
        # We initialize the DB
        db.initialize()
        # If all good we go scraping
        scrape_data(username=username, password=password, keyword=keyword, limit=args.limit)
    except FileNotFoundError:
        print(f"You must have a file called {config.AUTH_DB_FILE} with your MySQL credentials: "
              f"host, username and password each in a separate line.")


if __name__ == "__main__":
    main()
