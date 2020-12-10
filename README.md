# Welcome to Insta Scraper!

## 1. About the project
Insta scraper is a command-line application written in Python that scrapes public Instagram information about:
  * Users (username, followers, following, etc)
  * Posts (likes, views, etc)
  * Hashtags
  * Locations
  
It is fully automated and stores all the information into a MySQL database.

**IMPORTANT** : You need to have a file called db_auth.txt with your MySQL credentials (see instructions section below)

### Built with:
* Python 
* MySQL

## 2. Getting Startted

### Installation
```
pip install requests
pip install beautifulsoup4
pip install selenium
pip install mysql-connector-python
```
### Pre-requisites
You must create a file called db_auth.txt in which to add your MySQL credentials separated by line breaks.

Example db_auth.txt:
```
localhost
mysqluser
mysqlpass
```

Additionally you can create a file called auth.txt with your Instagram credentials (optional)

Example auth.txt:
```
myinstauser
myinstapass
```
**Not to worry, your data is not stored anywhere**

## 3. Usage

The program can be run in two ways from Terminal:
 * a. Via the interactive menu. The authentication is part of the process. No arguments required.
 * b. Via arguments. The authentication will be done either from `filename` provided as an argument or from default file named `auth.txt`.
  
 > Note: Arguments mode is launched with `-k KEYWORD` argument. Once provided the programm will run in this mode.

**NOTE**: To scrape a private user's media you must be an approved follower.

For help please type
```sh
> python insta.py -h

usage: insta.py [-h] [-k KEYWORD] [-f FILENAME] [-l LIMIT]

scrape instagram by keyword (hashtag or username)

optional arguments:
  -h, --help            show this help message and exit
  -k KEYWORD, --keyword KEYWORD
                        the keyword to find in instagram (by #hashtag or @username)
  -f FILENAME, --filename FILENAME
                        option for logging in through a file username must be in the first line and password in the second one
  -l LIMIT, --limit LIMIT
                        limit of instagram posts to scrap
   ```


### a. Interactive mode example
Run through nice interactive UI
  
```sh
> python insta.py
```
Then, follow the guidelines

### b. Argument mode example

Searching via hashtag (with a #)
```
> python insta.py -k #cats 
```

Searching via username (with a @)
```
> python insta.py -k @therock
```

Spcifying a different auth filename and a limit of posts to scrape 
```
> python insta.py -k #food -f credentials.txt -l 500 
```

## 4. Database

### Entity Relationship Diagram
![GitHub Logo](/erd.png)

>NOTE: In order to store the information you scrape to the database you need to have a file named `db_auth.txt` in your project directory.

`db_auth.txt` must include (written in three separate lines):
* localhost
* root
* personal password to your MySQL

## 5. Logging

Every Database insertion is logged into ```insta_scraper.log```


**NOTE:** Each log comes with its log level (DEGUB, INFO, WARNING, etc)

By default logs will be printed BOTH to console and the log file *.log file but this can be easily changed for each situation.

Log message example:
```
2020-11-28 21:59:27,804 - INFO - Created Hashtag: chile
```  
## 6. API usage

When users upload posts they usually add a Location attribute. With this we do 2 things:
 * We get the Geo Coordinates of the Location using [Google Geo Location API](https://developers.google.com/maps/documentation/geolocation/overview)
 * We get the weather Forecast and avergae Temperature on the day of the post using [Weather API](https://www.weatherapi.com/)
 
We added these columns to the respective tables.

You need to have a file called ```api_keys.py``` with this format:
```
API_KEY_GEO = "<your_google_api_key>"
API_KEY_WEATHER = "<your_weather_api_key>"
```
 
 
 




