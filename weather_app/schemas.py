from pydantic import BaseModel
from typing import List


class CityWeather(BaseModel):
    city: str
    parameters: str

class FewCityWeather(BaseModel):
    cities: List[str]
    parameters: str