from Gku import settings
import requests

def getCoord(adress):
    URL = 'https://geocode-maps.yandex.ru/1.x/'
    PARAMS = {'apikey': settings.YANDEX_API_GEOCODE_KEY, 'geocode': adress, 'format': 'json'}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    return data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']