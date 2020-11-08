# Insta Scraper

Insta scraper is a command-line application written in Python that scrapes information about
  * Number of likes 
  * Number of comments
  * Hashtags
  * Link to the post
  * Username 
It is fully automated, uses  BeautifulSoup and Selenium modules (please see requirements.txt for further information)

Safe provision of the username and the password can be done in two ways:
  * Via the interactive menu
  * From an authentication file (by default it is named auth.txt)

**Not to worry, your data is not stored anywhere**

**NOTE**: To scrape a private user's media you must be an approved follower.

For help please type
```sh
> python insta.py -h

usage: insta.py [-h] [-i | -k KEYWORD] [-f FILENAME] [-l LIMIT]

scrape instagram by keyword (hashtag)

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     run through nice interactive ui
  -k KEYWORD, --keyword KEYWORD
                        the keyword to find in instagram (by #hashtag or @username)
  -f FILENAME, --filename FILENAME
                        option for logging in through a file username must be in the first line and password in the second one
  -l LIMIT, --limit LIMIT
                        limit of instagram posts to scrap
   ```


## Interactive mode example  
```sh
> python insta.py -i
```
Then, follow the guidelines

## Argument mode example
```sh
> python insta.py -k #cats -f credentials.txt -l 500 

```

