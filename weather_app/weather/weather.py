from pydantic import BaseModel, Field
from typing import List, Union
from datetime import datetime

class Coord(BaseModel):
    lon: float
    lat: float

class ShortWeatherInfo(BaseModel):
    id: int
    main: str
    description: str
    icon: str

class MainWeatherInfo(BaseModel):
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    temp_min: float
    temp_max: float
    sea_level: Union[None, int]
    grnd_level: Union[None, int]

class Wind(BaseModel):
    speed: float
    deg: int
    gust: Union[None, float]

class Rain(BaseModel):
    high_one: Union[float, None] = Field(alias="1h")
    high_three: Union[float, None] = Field(alias="3h")

class Snow(BaseModel):
    high_one: Union[float, None] = Field(alias="1h")
    high_three: Union[float, None] = Field(alias="3h")

class Clouds(BaseModel):
    all: int

class OpenApiSys(BaseModel):
    type: int
    id: int
    country: str
    sunrise: datetime
    sunset: datetime

class Weather(BaseModel):
   coord: Coord
   weather: List[ShortWeatherInfo]
   base: str
   main: MainWeatherInfo
   visibility: int
   wind: Union[None, Wind]
   rain: Union[None, Rain]
   clouds: Union[None, Clouds]
   snow: Union[None, Snow]
   dt: datetime
   timezone: datetime
   sys: OpenApiSys
   id: int
   name: str
   cod: int