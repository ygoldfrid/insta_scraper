import time
import requests
import config
import api_keys


def google_geo_api(address):
    base_url = config.GOOGLE_GEO_BASE

    params = {
        'key': api_keys.API_KEY_GEO,
        'address': address
    }

    response = requests.get(base_url, params=params).json()
    if response['status'] == 'OK':
        geometry = response['results'][0]['geometry']
        lat = geometry['location']['lat']
        lon = geometry['location']['lng']
    else:
        return None, None

    return lat, lon


def get_weather_api(address):
    lat, lon = google_geo_api(address)
    params = {'lat': lat,
              'lon': lon,
              'appid': api_keys.API_KEY_WEATHER,
              'units': 'metric'
              }

    url = config.WEATHER
    res = requests.get(url, params=params).json()

    temp = res['main']['temp']

    latitude = res['coord']['lat']
    longitude = res['coord']['lon']

    description = res['weather'][0]['description']

    return temp, latitude, longitude, description


test = r"Jerusalem, Israel"
data = get_weather_api(address=test)
print(data)
