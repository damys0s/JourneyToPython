from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from citypulse.domain import CityData, CityDataNotFound, Pollution, Weather


def test_citydata_creation_success() -> None:
    weather = Weather(
        temperature=25.0,
        humidity=60.0,
        pressure=1015.0,
        date=datetime.now(),
    )
    pollution = Pollution(
        pm10=15.0, pm25=10.0, no2=30.0, so2=20.0, co=0.8, date=datetime.now()
    )
    city_data = CityData(city="TestCity", weather=weather, pollution=pollution)

    assert city_data.city == "TestCity"
    assert city_data.weather.temperature == 25.0
    assert city_data.weather.humidity == 60.0
    assert city_data.weather.pressure == 1015.0
    assert city_data.pollution.pm10 == 15.0
    assert city_data.pollution.pm25 == 10.0
    assert city_data.pollution.no2 == 30.0
    assert city_data.pollution.so2 == 20.0
    assert city_data.pollution.co == 0.8


def test_citydatanotfound_contains_city() -> None:
    exception = CityDataNotFound("MissingCity")
    assert "MissingCity" in str(exception)
    assert exception.city == "MissingCity"


def test_update_citydata_immutable() -> None:
    weather = Weather(
        temperature=20.0,
        humidity=50.0,
        pressure=1013.0,
        date=datetime.now(),
    )
    pollution = Pollution(
        pm10=10.0, pm25=5.0, no2=20.0, so2=15.0, co=0.5, date=datetime.now()
    )
    citydata = CityData(city="ImmutableCity", weather=weather, pollution=pollution)

    with pytest.raises(FrozenInstanceError):
        setattr(citydata, "city", "NewCity")  # noqa: B010

    with pytest.raises(FrozenInstanceError):
        setattr(citydata.pollution, "pm10", 25.0)  # noqa: B010
