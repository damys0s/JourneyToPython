from .domain import (
    CityData,
    CityDataNotFound,
)
from .repositories import CityPulseRepository


def get_city_data(repo: CityPulseRepository, city: str) -> CityData:
    data = repo.get_city_data(city)
    if data is None:
        raise CityDataNotFound(city)
    return data


def add_city_data(repo: CityPulseRepository, city_data: CityData) -> None:
    repo.add_city_data(city_data)


def update_city_data(repo: CityPulseRepository, city_data: CityData) -> None:
    existing = repo.get_city_data(city_data.city)
    if existing is None:
        raise CityDataNotFound(city_data.city)
    repo.update_city_data(city_data)


def delete_city_data(repo: CityPulseRepository, city: str) -> None:
    existing = repo.get_city_data(city)
    if existing is None:
        raise CityDataNotFound(city)
    repo.delete_city_data(city)


def list_cities(repo: CityPulseRepository) -> list[str]:
    return repo.list_cities()
