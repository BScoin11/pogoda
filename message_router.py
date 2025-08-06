from aiogram import Router
from aiogram.filters import Command,StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import F
import os
import  httpx
from typing import Dict, Any
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    kb = [
        [
            KeyboardButton(text="погода")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите погоду"
    )
    await message.answer("выберете вариант погоды", reply_markup=keyboard)




class State_weather_user(StatesGroup):
    choosing_weather = State()


@router.message(F.text.lower() == "погода", StateFilter(None))
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
        await message.answer(f'Температура {TempAirEnv}\n Осадки {PrecipMM}\n Скорость ветра {WindKph}')
        print(url_get_weatherapi)
    except KeyError:
        await message.answer("Такого города не существует")


