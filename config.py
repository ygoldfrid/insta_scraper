# Basic info
BASE_URL = "https://www.instagram.com/"
DB_FILENAME = 'insta.db'

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

# Authentication process selectors
AUTH_USER_SEL = "input[name='username']"
AUTH_PASS_SEL = "input[name='password']"
SUBMIT_SELECTOR = "button[type='submit']"
NOT_NOW_XPATH = "//button[contains(text(), 'Not Now')]"
SEARCH_XPATH = "//input[@placeholder='Search']"


def hash_xpath(keyword):
    """
    Returns the xpath of the hashtag button wew need to click on
    :param keyword: the hashtag or username that the user wrote
    :return: xpath of the button
    """
    return f"//span[contains(text(), '{keyword}')]"



