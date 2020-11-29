# Insta Scraper

Insta scraper is a command-line application written in Python that scrapes information about:
  * Users
  * Posts
  * Hashtags
  * Locations
  
It is fully automated, it uses Requests, BeautifulSoup and Selenium modules (please see requirements.txt for further information) and stores all the data into a MySQL database.

**IMPORTANT** : You need to have a file called db_auth.txt with your MySQL credentials (see Database section below)

The program can be run in two ways from Terminal:
  * Via the interactive menu. The authentication is part of the process. No arguments required.
  * Via arguments. The authentication will be done either from `filename` provided as an argument or from default file named "./auth.txt".
  > Note: Arguments mode is launched with `keyword` argument. Once provided the programm will run in this mode.

**Not to worry, your data is not stored anywhere**

**NOTE**: To scrape a private user's media you must be an approved follower.

For help please type
```sh
> python insta.py -h

usage: insta.py [-h] [-k KEYWORD] [-f FILENAME] [-l LIMIT]

scrape instagram by keyword (hashtag)

optional arguments:
  -h, --help            show this help message and exit
  -k KEYWORD, --keyword KEYWORD
                        the keyword to find in instagram (by #hashtag or @username)
  -f FILENAME, --filename FILENAME
                        option for logging in through a file username must be in the first line and password in the second one
  -l LIMIT, --limit LIMIT
                        limit of instagram posts to scrap
   ```


## Interactive mode example
Run through nice interactive UI
  
```sh
> python insta.py
```
Then, follow the guidelines

## Argument mode example
```sh
> python insta.py -k #cats -f credentials.txt -l 500 
```

## Database support

![GitHub Logo](/erd.png)

>NOTE: In order to store the information you scrape to the database you need to have a file named `db_auth.txt` in your project directory.

`db_auth.txt` must include (written in three separate lines):
* localhost
* root
* personal password to your MySQL

## Logging

Logging option is introduced to the functionality of the scraper. 


**NOTE:** it is necessary to provide log level (for example INFO and the message that will be printed)

Default option is to print logs BOTH to console and the *.log file but this can be easily changed for each situation.

For example, to log Error output to the file the following command is needed:

```
logger.log(logging.ERROR, msg="File not found", destination=logger.FILE)
```  





