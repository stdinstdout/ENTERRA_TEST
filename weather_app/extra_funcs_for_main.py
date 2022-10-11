import asyncio
import aiohttp
from functools import lru_cache

from .weather.weather_request import WeatherRequest
from .weather.weather import Weather
from .config import Settings
from .schemas import GetCity


@lru_cache()
def get_settings():
    return Settings()


def get_city_include_fields(weather: Weather, params):
    res = GetCity(city=weather.name)  # type: ignore
    if 'temperature' in params:
        res.temperature = weather.main.temp
    if 'feels' in params:
        res.feels = weather.main.feels_like
    if 'wind' in params:
        res.wind = weather.wind.dict()  # type: ignore
    if 'visibility' in params:
        res.visibility = weather.visibility
    if 'humidity' in params:
        res.humidity = weather.main.humidity

    return res


async def async_request_city_weather(cities):
    async with aiohttp.ClientSession() as session:
        tasks = [WeatherRequest(city).async_request(session) for city in cities]
        result = await asyncio.gather(*tasks)
        return result
