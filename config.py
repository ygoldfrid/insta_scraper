# Basic info
BASE_URL = "https://www.instagram.com/"
AUTH_DB_FILE = 'db_auth.txt'

# Scraping process selectors
POST_SELECTOR_BY_USER = "#react-root > section > main > div > div._2z6nI > article > div:nth-child(1) >" \
                        " div > div:nth-child(1) > div:nth-child(1) > a"
POST_SELECTOR_BY_HASH = "#react-root > section > main > article > div.EZdmt > div > div >" \
                        " div:nth-child(1) > div:nth-child(1) > a"
USER_SELECTOR = "body > div._2dDPU.CkGkG > div.zZYga > div > article > header > div.o-MQd.z8cbW >" \
                " div.PQo_0.RqtMr > div.e1e1d > span > a"
LINK_SELECTOR = "body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.k_Q0X.NnvRN > a"
LIKES_SELECTOR = "body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.EDfFK.ygqzn > div"
HASH_SELECTOR = "body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > div >" \
                " li > div > div > div.C4VMK"
LOCATION_SELECTOR = "body > div._2dDPU.CkGkG > div.zZYga > div > article > header > div.o-MQd.z8cbW >" \
                    " div.M30cS > div.JF9hh"
NEXT_POST_CLASS = "coreSpriteRightPaginationArrow"
DATA_TO_JSON = "?__a=1"

# Authentication process selectors
AUTH_USER_SEL = "input[name='username']"
AUTH_PASS_SEL = "input[name='password']"
SUBMIT_SELECTOR = "button[type='submit']"
NOT_NOW_XPATH = "//button[contains(text(), 'Not Now')]"
SEARCH_XPATH = "//input[@placeholder='Search']"

#API
GOOGLE_GEO_BASE = 'https://maps.googleapis.com/maps/api/geocode/json?'
WEATHER = 'http://api.openweathermap.org/data/2.5/weather?'
WEATHER2 = "http://api.weatherapi.com/v1/history.json"



def hash_xpath(keyword):
    """
    Returns the xpath of the hashtag button wew need to click on
    :param keyword: the hashtag or username that the user wrote
    :return: xpath of the button
    """
    return f"//span[contains(text(), '{keyword}')]"



