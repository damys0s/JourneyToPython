from __future__ import annotations

from datetime import datetime

import pytest

from citypulse.domain import CityData, CityDataNotFound, Pollution, Weather
from citypulse.services import get_city_data


class FakeCityPulseRepo:
    def __init__(self) -> None:
        self._data: dict[str, CityData] = {}

    def add_city_data(self, city_data: CityData) -> None:
        self._data[city_data.city] = city_data

    def get_city_data(self, city: str) -> CityData | None:
        return self._data.get(city)

    def update_city_data(self, city_data: CityData) -> None:
        if city_data.city in self._data:
            self._data[city_data.city] = city_data

    def delete_city_data(self, city: str) -> bool:
        return self._data.pop(city, None) is not None

    def list_cities(self) -> list[str]:
        return list(self._data.keys())


def test_get_city_data_success() -> None:
    repo = FakeCityPulseRepo()
    city_data = CityData(
        city="Testville",
        weather=Weather(
            temperature=20.0,
            humidity=50.0,
            pressure=1013.0,
            date=datetime.now(),
        ),
        pollution=Pollution(
            pm10=10.0,
            pm25=5.0,
            no2=20.0,
            so2=15.0,
            co=0.5,
            date=datetime.now(),
        ),
    )
    repo.add_city_data(city_data)

    result = get_city_data(repo, "Testville")

    assert result == city_data
    assert result.city == "Testville"


def test_get_city_data_not_found() -> None:
    repo = FakeCityPulseRepo()

    with pytest.raises(CityDataNotFound):
        get_city_data(repo, "UnknownCity")
