from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Weather:
    temperature: float
    humidity: float
    pressure: float
    date: datetime


@dataclass(frozen=True, slots=True)
class Pollution:
    pm10: float
    pm25: float
    no2: float
    so2: float
    co: float
    date: datetime


@dataclass(frozen=True, slots=True)
class CityData:
    city: str
    weather: Weather
    pollution: Pollution


@dataclass
class CityDataNotFound(Exception):
    def __init__(self, city: str) -> None:
        super().__init__(f"City data not found for {city}")
        self.city = city


@dataclass
class CityDataAlreadyExists(Exception):
    def __init__(self, city: str) -> None:
        super().__init__(f"City data for {city} already exists")
        self.city = city
