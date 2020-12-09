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
        raise Exception("Unable to get location")

    return lat, lon


def get_weather_api(latitude, lontitude, address):
    params = {'lat': latitude,
              'lon': lontitude,
              'appid': api_keys.API_KEY_WEATHER,
              'units': 'metric'
              }

    url = config.WEATHER
    res = requests.get(url, params=params).json()
    if res['cod'] == 200:
        temp = res['main']['temp']
        latitude = res['coord']['lat']
        longitude = res['coord']['lon']
        description = res['weather'][0]['main']
        return temp, latitude, longitude, description
    else:
        raise Exception("Unable to get weather details")


test = r"Jerusalem, Israel"
lat, lon = google_geo_api(address=test)
data = get_weather_api(latitude=lat, lontitude=lon, address=test)
print(data)
