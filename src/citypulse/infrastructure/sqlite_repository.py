import sqlite3

from citypulse.domain import CityData, Pollution, Weather


class SqliteCityRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.ensure_schema()

    def connect(self):
        """Retourne une connexion SQLite sur le fichier cible."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def ensure_schema(self):
        """Créée la table CityData si elle n'existe pas déjà."""
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS city_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT UNIQUE NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS weather (
                    city_id INTEGER PRIMARY KEY,
                    temperature REAL NOT NULL,
                    humidity REAL NOT NULL,
                    pressure REAL NOT NULL,
                    FOREIGN KEY (city_id) REFERENCES city_data(id) ON DELETE CASCADE
                    )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS pollution (
                    city_id INTEGER PRIMARY KEY,
                    pm10 REAL NOT NULL,
                    pm25 REAL NOT NULL,
                    no2 REAL NOT NULL,
                    so2 REAL NOT NULL,
                    co REAL NOT NULL,
                    FOREIGN KEY (city_id) REFERENCES city_data(id) ON DELETE CASCADE
                    )
                """
            )

    def get_city_data(self, city: str) -> CityData | None:
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT cd.city, w.temperature, w.humidity, w.pressure, "
                "p.pm10, p.pm25, p.no2, p.so2, p.co FROM city_data cd "
                "JOIN weather w ON w.city_id = cd.id "
                "JOIN pollution p ON p.city_id = cd.id "
                "WHERE cd.city = ?",
                (city,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return CityData(
                city=row[0],
                weather=Weather(temperature=row[1], humidity=row[2], pressure=row[3]),
                pollution=Pollution(
                    pm10=row[4], pm25=row[5], no2=row[6], so2=row[7], co=row[8]
                ),
            )

    def add_city_data(self, city_data) -> None:
        with self.connect() as conn:
            # Si city_data existe déjà:
            if self.get_city_data(city_data.city) is None:
                conn.execute(
                    """
                    INSERT INTO city_data (city) VALUES (?)
                    """,
                    (city_data.city,),
                )
                conn.execute(
                    """
                    INSERT INTO weather (city_id, temperature, humidity, pressure) 
                    VALUES (
                        (SELECT id FROM city_data WHERE city = ?),
                        ?, ?, ?
                    )
                    """,
                    (
                        city_data.city,
                        city_data.weather.temperature,
                        city_data.weather.humidity,
                        city_data.weather.pressure,
                    ),
                )
                conn.execute(
                    """
                    INSERT INTO pollution (city_id, pm10, pm25, no2, so2, co) VALUES (
                        (SELECT id FROM city_data WHERE city = ?), ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        city_data.city,
                        city_data.pollution.pm10,
                        city_data.pollution.pm25,
                        city_data.pollution.no2,
                        city_data.pollution.so2,
                        city_data.pollution.co,
                    ),
                )

    def update_city_data(self, city_data: CityData) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE weather SET temperature = ?, humidity = ?, pressure = ?
                WHERE city_id = (SELECT id FROM city_data WHERE city = ?)
                """,
                (
                    city_data.weather.temperature,
                    city_data.weather.humidity,
                    city_data.weather.pressure,
                    city_data.city,
                ),
            )
            conn.execute(
                """
                UPDATE pollution SET pm10 = ?, pm25 = ?, no2 = ?, so2 = ?, co = ?
                WHERE city_id = (SELECT id FROM city_data WHERE city = ?) 
                """,
                (
                    city_data.pollution.pm10,
                    city_data.pollution.pm25,
                    city_data.pollution.no2,
                    city_data.pollution.so2,
                    city_data.pollution.co,
                    city_data.city,
                ),
            )

    def delete_city_data(self, city: str) -> bool:
        with self.connect() as conn:
            cursor = conn.execute("DELETE FROM city_data WHERE city = ?", (city,))
            return cursor.rowcount > 0

    def list_cities(self) -> list[str]:
        with self.connect() as conn:
            cursor = conn.execute("SELECT city FROM city_data")
            return [row[0] for row in cursor.fetchall()]
