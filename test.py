import  httpx
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

weatherapi_keys_env = (os.getenv('WEATHERAPIKEY'))

def test_funk(weatherapi_keys :str, location_lat :str):

    url_get_weatherapi = "http://api.weatherapi.com/v1/current.json?key=" + str(weatherapi_keys) + "%20&q=" + str(
        location_lat) + "&aqi=no&lang=" + str("ru")
    get_weatherapi = httpx.get(url_get_weatherapi, timeout=10)
    get_weatherapi_temp = get_weatherapi.json()["current"]["feelslike_c"]
    TempAirEnv = (get_weatherapi_temp)
    TempAirEnv = int(TempAirEnv)
    TempAirEnv = str(TempAirEnv)

    return TempAirEnv

res = test_funk(weatherapi_keys_env, 'Краснодар')
print(res)