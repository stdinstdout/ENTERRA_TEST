from fastapi_redis_cache import FastApiRedisCache, cache_one_hour
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI, Request, Response

from sqlalchemy.orm import Session
from functools import lru_cache

from .extra_funcs_for_main import get_need_field, task
from .schemas import CityWeather, FewCityWeather
from .weather import WeatherRequest
from .config import Settings


app = FastAPI()
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)

@lru_cache()
def get_settings():
    return Settings()


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=get_settings().LOCAL_REDIS_URL,
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Request, Response, Session]
    )
    

@app.get('/one_city_weather')
@cache_one_hour()
def city_weather(city_weather: CityWeather):
    city = city_weather.city
    params = set(city_weather.parameters.split(' '))
    wr = WeatherRequest(city)
    return get_need_field(wr.get_weather(), params)
    

@app.get('/many_city_weather')
@cache_one_hour()
async def fewcity_weather(few_city_weather: FewCityWeather):
    cities = few_city_weather.cities
    params = set(few_city_weather.parameters.split(' '))
    res = await task(cities)
    return [get_need_field(r, params) for r in res]

    

    
