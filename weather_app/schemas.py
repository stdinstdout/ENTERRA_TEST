from pydantic import BaseModel
from typing import List, Union

from .weather.weather import Wind

class CityWeather(BaseModel):
    city: str
    parameters: str

class CitiesWeather(BaseModel):
    cities: List[str]
    parameters: str

class GetCity(BaseModel):
    city: str
    temperature: Union[None, float]
    feels: Union[None, float]
    wind: Union[None, dict]
    visibility: Union[None, int]
    humidity: Union[None, int]


