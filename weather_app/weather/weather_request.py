from pydantic import ValidationError
from fastapi import HTTPException
from functools import lru_cache
import requests

from weather_app.config import Settings
from .weather import Weather

@lru_cache()
def get_settings():
    return Settings() 


class WeatherRequest:
    def __init__(self, 
                city,
                units='metric',
                lang='ru',
                url='https://api.openweathermap.org/data/2.5/weather/'):
        self.appid = get_settings().API_KEY
        self.url = url
        self.city = city
        self.units = units
        self.lang = lang


    def _request(self):
        r = requests.get(url=self.url,
                        params={
                            'appid': self.appid,
                            'q': self.city,
                            'units': self.units,
                            'lang': self.lang,
                        })
        print(r.request.path_url)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.json()['message'])
        else:
            return r.text

    
    async def async_request(self, session):
        url = f"{self.url}?appid={self.appid}&q={self.city}"
        async with session.get(url) as response:
            try:
                return Weather.parse_raw(await response.text())
            except ValidationError as e:
                raise HTTPException(status_code=402,detail="Город не найден или полученные данные не валидны")



    def get_weather(self):
        return Weather.parse_raw(self._request())
        