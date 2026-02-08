from datetime import datetime

import pytest

from citypulse.domain import CityData, CityDataNotFound, Pollution, Weather
from citypulse.infrastructure.sqlite_repository import SqliteCityRepository


def test_add_and_list_cities(tmp_path) -> None:
    db_file = tmp_path / "citypulse.db"
    repo = SqliteCityRepository(str(db_file))

    city_data = CityData(
        city="Testville",
        weather=Weather(
            temperature=20.0, humidity=60.0, pressure=1013.25, date=datetime.now()
        ),
        pollution=Pollution(
            pm10=50.0, pm25=25.0, no2=40.0, so2=15.0, co=1.5, date=datetime.now()
        ),
    )

    repo.add_city_data(city_data)
    cities = repo.list_cities()
    assert cities == ["Testville"]


def test_get_city_data(tmp_path) -> None:
    db_file = tmp_path / "citypulse.db"
    repo = SqliteCityRepository(str(db_file))

    city_data = CityData(
        city="Testville",
        weather=Weather(
            temperature=20.0, humidity=60.0, pressure=1013.25, date=datetime.now()
        ),
        pollution=Pollution(
            pm10=50.0, pm25=25.0, no2=40.0, so2=15.0, co=1.5, date=datetime.now()
        ),
    )

    repo.add_city_data(city_data)
    assert repo.get_city_data("Testville") == city_data


def test_update_city_data(tmp_path) -> None:
    db_file = tmp_path / "citypulse.db"
    repo = SqliteCityRepository(str(db_file))

    city_data = CityData(
        city="Testville",
        weather=Weather(
            temperature=20.0, humidity=60.0, pressure=1013.25, date=datetime.now()
        ),
        pollution=Pollution(
            pm10=50.0, pm25=25.0, no2=40.0, so2=15.0, co=1.5, date=datetime.now()
        ),
    )

    repo.add_city_data(city_data)

    updated_data = CityData(
        city="Testville",
        weather=Weather(
            temperature=25.0, humidity=65.0, pressure=1013.25, date=datetime.now()
        ),
        pollution=Pollution(
            pm10=60.0, pm25=30.0, no2=45.0, so2=20.0, co=2.0, date=datetime.now()
        ),
    )

    repo.update_city_data(updated_data)

    assert repo.get_city_data("Testville") == updated_data


def test_delete_city_data(tmp_path) -> None:
    db_file = tmp_path / "citypulse.db"
    repo = SqliteCityRepository(str(db_file))

    city_data = CityData(
        city="Testville",
        weather=Weather(
            temperature=20.0, humidity=60.0, pressure=1013.25, date=datetime.now()
        ),
        pollution=Pollution(
            pm10=50.0, pm25=25.0, no2=40.0, so2=15.0, co=1.5, date=datetime.now()
        ),
    )

    repo.add_city_data(city_data)
    repo.delete_city_data("Testville")
    retrieved = repo.get_city_data("Testville")
    assert retrieved is None


def test_list_cities(tmp_path) -> None:
    db_file = tmp_path / "citypulse.db"
    repo = SqliteCityRepository(str(db_file))

    city_data = CityData(
        city="Testville",
        weather=Weather(
            temperature=20.0, humidity=60.0, pressure=1013.25, date=datetime.now()
        ),
        pollution=Pollution(
            pm10=50.0, pm25=25.0, no2=40.0, so2=15.0, co=1.5, date=datetime.now()
        ),
    )

    city_data2 = CityData(
        city="Testville2",
        weather=Weather(
            temperature=30.0, humidity=65.0, pressure=1013.25, date=datetime.now()
        ),
        pollution=Pollution(
            pm10=50.0, pm25=27.0, no2=40.0, so2=15.0, co=1.5, date=datetime.now()
        ),
    )

    repo.add_city_data(city_data)
    repo.add_city_data(city_data2)

    cities = repo.list_cities()
    assert set(cities) == {"Testville", "Testville2"}


def test_update_city_not_existing(tmp_path) -> None:
    db_file = tmp_path / "citypulse.db"
    repo = SqliteCityRepository(str(db_file))

    city_data = CityData(
        city="NonExistingCity",
        weather=Weather(
            temperature=20.0, humidity=60.0, pressure=1013.25, date=datetime.now()
        ),
        pollution=Pollution(
            pm10=50.0, pm25=25.0, no2=40.0, so2=15.0, co=1.5, date=datetime.now()
        ),
    )

    with pytest.raises(CityDataNotFound):
        repo.update_city_data(city_data)

    assert repo.get_city_data("NonExistingCity") is None


def test_delete_city_not_existing(tmp_path) -> None:
    db_file = tmp_path / "citypulse.db"
    repo = SqliteCityRepository(str(db_file))

    assert not repo.delete_city_data("NonExistingCity")
