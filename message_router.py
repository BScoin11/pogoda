from aiogram import Router
from aiogram.filters import Command,StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import F
import os
import  httpx
from typing import Dict, Any

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"hello world!")

@router.message(F.text.lower() == "погода")
async def cmd_weather(message: Message):
    location_lat = (os.getenv('LAT_LON'))
    weatherapi_keys = (os.getenv('WEATHERAPIKEY'))
    url_get_weatherapi = "http://api.weatherapi.com/v1/current.json?key=" + str(weatherapi_keys) + "%20&q=" + str(
        location_lat) + "&aqi=no&lang=" + str("ru") + "ru"
    get_weatherapi = httpx.get(url_get_weatherapi, timeout=10)
    get_weatherapi_temp = get_weatherapi.json()["current"]["feelslike_c"]
    get_weatherapi_precip_mm = get_weatherapi.json()["current"]["precip_mm"]
    get_weatherapi_location_name = get_weatherapi.json()["location"]["name"]
    TempAirEnv = (get_weatherapi_temp)
    LocationRu = (get_weatherapi_location_name)
    TempAirEnv = int(TempAirEnv)
    TempAirEnv = str(TempAirEnv)
    PrecipMM =  str(get_weatherapi_precip_mm)
    #PrecipMM = str(PrecipMM)
    #await message.answer("Температура %s Осадки %s", TempAirEnv, PrecipMM)
    await message.answer(f'Температура {TempAirEnv} Осадки {PrecipMM}')
    print(url_get_weatherapi)



class State_weather_user(StatesGroup):
    choosing_weather = State()


@router.message(F.text.lower() == "погода2", StateFilter(None))
async def process_fillform_command_ltc(message: Message, state: FSMContext):
    bot_answer_text = await message.answer(text='Пожалуйста, введите Город')
    await state.set_state(State_weather_user.choosing_weather)


@router.message(StateFilter(State_weather_user.choosing_weather), F.text.isalpha())
async def process_name_sent_ltc(message: Message, state: FSMContext):
    data = await state.update_data(th_s_btc=message.text)
    await state.clear()
    bot_answer_text = await message.answer(
        "Ищу погодные условия ..."
    )
    await show_summary_ltc(message=message, data=data)




async def show_summary_ltc(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    try:
        location_lat = data["th_s_btc"]
        weatherapi_keys = (os.getenv('WEATHERAPIKEY'))
        url_get_weatherapi = "http://api.weatherapi.com/v1/current.json?key=" + str(weatherapi_keys) + "%20&q=" + str(location_lat) + "&aqi=no&lang=" + str("ru") + "ru"
        get_weatherapi = httpx.get(url_get_weatherapi, timeout=10)
        get_weatherapi_temp = get_weatherapi.json()["current"]["feelslike_c"]
        get_weatherapi_precip_mm = get_weatherapi.json()["current"]["precip_mm"]
        get_weatherapi_wind_kph = get_weatherapi.json()["current"]["wind_kph"]
        get_weatherapi_location_name = get_weatherapi.json()["location"]["name"]
        TempAirEnv = (get_weatherapi_temp)
        LocationRu = (get_weatherapi_location_name)
        TempAirEnv = int(TempAirEnv)
        TempAirEnv = str(TempAirEnv)
        PrecipMM = str(get_weatherapi_precip_mm)
        WindKph = str(get_weatherapi_wind_kph)
        await message.answer(f'Температура {TempAirEnv} Осадки {PrecipMM} Скорость ветра {WindKph}')
        print(url_get_weatherapi)
    except KeyError:
        await message.answer("Такого города не существует")