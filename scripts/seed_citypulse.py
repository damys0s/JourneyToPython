from __future__ import annotations

from datetime import datetime, timedelta

from citypulse.domain import CityData, Pollution, Weather
from citypulse.infrastructure.sqlite_repository import SqliteCityRepository


def build_measurements() -> list[CityData]:
    base = datetime(2026, 2, 8, 8, 0, 0)

    return [
        CityData(
            city="Lausanne",
            weather=Weather(temperature=3.2, humidity=82.0, pressure=1018.1, date=base),
            pollution=Pollution(
                pm10=18.0,
                pm25=11.0,
                no2=24.0,
                so2=3.0,
                co=0.4,
                date=base,
            ),
        ),
        CityData(
            city="Geneve",
            weather=Weather(temperature=4.1, humidity=79.0, pressure=1017.4, date=base),
            pollution=Pollution(
                pm10=21.0,
                pm25=13.0,
                no2=27.0,
                so2=4.0,
                co=0.5,
                date=base,
            ),
        ),
        CityData(
            city="Fribourg",
            weather=Weather(temperature=2.6, humidity=85.0, pressure=1018.8, date=base),
            pollution=Pollution(
                pm10=16.0,
                pm25=9.0,
                no2=20.0,
                so2=2.0,
                co=0.3,
                date=base,
            ),
        ),
        CityData(
            city="Neuchatel",
            weather=Weather(temperature=3.5, humidity=80.0, pressure=1017.9, date=base),
            pollution=Pollution(
                pm10=19.0,
                pm25=10.0,
                no2=22.0,
                so2=3.0,
                co=0.4,
                date=base,
            ),
        ),
        CityData(
            city="Sion",
            weather=Weather(temperature=5.9, humidity=69.0, pressure=1016.7, date=base),
            pollution=Pollution(
                pm10=23.0,
                pm25=14.0,
                no2=29.0,
                so2=4.0,
                co=0.5,
                date=base,
            ),
        ),
        # Follow-up observations to simulate refreshes
        CityData(
            city="Lausanne",
            weather=Weather(
                temperature=5.0,
                humidity=77.0,
                pressure=1017.8,
                date=base + timedelta(hours=3),
            ),
            pollution=Pollution(
                pm10=19.0,
                pm25=12.0,
                no2=23.0,
                so2=3.0,
                co=0.4,
                date=base + timedelta(hours=3),
            ),
        ),
        CityData(
            city="Geneve",
            weather=Weather(
                temperature=5.7,
                humidity=74.0,
                pressure=1017.2,
                date=base + timedelta(hours=3),
            ),
            pollution=Pollution(
                pm10=20.0,
                pm25=12.0,
                no2=26.0,
                so2=4.0,
                co=0.5,
                date=base + timedelta(hours=3),
            ),
        ),
    ]


def seed(db_path: str = "citypulse.db") -> None:
    repo = SqliteCityRepository(db_path)

    for measurement in build_measurements():
        try:
            repo.add_city_data(measurement)
        except Exception:
            repo.update_city_data(measurement)

    print("Seed complete")
    for city in repo.list_cities():
        print(city, repo.get_city_data(city))


if __name__ == "__main__":
    seed()
