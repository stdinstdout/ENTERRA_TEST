import asyncio
import aiohttp

from .weather.weather_request import WeatherRequest
from .weather.weather import Weather


def get_need_field(weather: Weather, params):
    res = {}
    res["city"] = weather.name
    if 'temperature' in params:
        res['temperature'] = weather.main.temp
    if 'feels' in params:
        res['feels'] = weather.main.feels_like
    if 'wind' in params:
        res['wind'] = weather.wind
    if 'visibility' in params:
        res['visibility'] = weather.visibility
    if 'humidity' in params:
        res['humidity'] = weather.main.humidity
    return res


async def task(cities):
    async with aiohttp.ClientSession() as session:
        tasks = [WeatherRequest(city).async_request(session) for city in cities]
        result = await asyncio.gather(*tasks)
        return result