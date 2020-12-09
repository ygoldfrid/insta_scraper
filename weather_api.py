import requests
import config
import api_keys
import logging
import logger


def google_geo(address):
    params = {
        'key': api_keys.API_KEY_GEO,
        'address': address
    }

    response = requests.get(config.GOOGLE_GEO_BASE, params=params).json()

    if response['status'] != 'OK':
        raise Exception("Unable to get location")

    geometry = response['results'][0]['geometry']
    lat = geometry['location']['lat']
    lon = geometry['location']['lng']

    return lat, lon


def get_weather(latitude, longitude, timestamp):
    params = {'key': api_keys.API_KEY_WEATHER,
              'q': f"{latitude},{longitude}",
              'unixdt': timestamp }

    response = requests.get(config.WEATHER2, params=params).json()

    if 'error' in response:
        logger.log(logging.WARNING, msg=response['error']['message'])
        return None, None
    else:
        temperature = response['forecast']['forecastday'][0]['day']['avgtemp_c']
        description = response['forecast']['forecastday'][0]['day']['condition']['text']
        return temperature, description
