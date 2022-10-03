from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import Depends, FastAPI

from functools import lru_cache

from .extra_funcs_for_main import get_city_include_fields, task
from .schemas import CityWeather, CitiesWeather, GetCity
from .weather import WeatherRequest
from .config import Settings


from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend


app = FastAPI()
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)

@lru_cache()
def get_settings():
    return Settings()

def redis_cache():
    return caches.get(CACHE_KEY)


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend(get_settings().LOCAL_REDIS_URL)
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()


@app.get('/city_weather')
async def city_weather(city_weather: CityWeather, cache: RedisCacheBackend = Depends(redis_cache)):
    city = city_weather.city
    params = set(city_weather.parameters.split(' '))

    in_cache = await cache.get(city)
    if in_cache:
        return GetCity.parse_raw(in_cache)

    wr = WeatherRequest(city)
    weather_city = get_city_include_fields(wr.get_weather(), params)

    await cache.set(key=city, value=weather_city.json())
    await cache.expire(key=city, ttl=get_settings().STORE_CACHE_TIME)

    return weather_city
    

@app.get('/cities_weather')
async def cities_weather(cities_weather: CitiesWeather, cache: RedisCacheBackend = Depends(redis_cache)):
    params = set(cities_weather.parameters.split(' '))
    cities = cities_weather.cities
    cached_cities = []
    not_cached_cities = []

    for city in cities:
        in_cache = await cache.get(city)
        if in_cache:
            cached_cities.append(GetCity.parse_raw(in_cache))
        else:
            not_cached_cities.append(city)

    got_cities = await task(not_cached_cities)
    for city in got_cities:
        gc = get_city_include_fields(city, params) 
        await cache.set(key=gc.city, value=gc.json())
        await cache.expire(key=gc.city, ttl=get_settings().STORE_CACHE_TIME)
        cached_cities += gc

    return cached_cities

    

    
