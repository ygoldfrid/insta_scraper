# Insta Scraper

Insta scraper is a command-line application written in Python that scrapes information about
  * Number of likes 
  * Number of comments
  * Hashtags
  * Link to the post
  * Username 
It is fully automated, uses  BeautifulSoup and Selenium modules (please see requirements.txt for further information)

The programm can be run in two ways from Terminal:
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



