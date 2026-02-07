import sqlite3

from journey_to_python.domain import Person, PersonId, PersonNotFound
from journey_to_python.repositories import PeopleRepository


class SQLitePeopleRepository(PeopleRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.ensure_schema()

    def _connect(self):
        """Retourne une connexion SQLite sur le fichier cible."""
        return sqlite3.connect(self.db_path)

    def ensure_schema(self):
        """Crée la table 'people' si elle n'existe pas déjà."""
        with self._connect() as conn:
            # Modèle relationnel simple:
            # - people: données principales
            # - emails: table enfant 1-N
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS people (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    active INTEGER NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS emails (
                person_id TEXT NOT NULL,
                email TEXT NOT NULL,
                PRIMARY KEY (person_id, email),
                FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE
                )
                """
            )

    def row_to_person(self, row) -> Person:
        """Convertit une ligne de la table 'people' en objet Person."""
        person_id, name, address, active = row
        with self._connect() as conn:
            emails = conn.execute(
                "SELECT email FROM emails WHERE person_id = ?", (person_id,)
            ).fetchall()
        return Person(
            id=PersonId(person_id),
            name=name,
            address=address,
            active=bool(active),
            emails=tuple(email for (email,) in emails),
        )

    def add(self, person: Person) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO people (id, name, address, active)
                VALUES (?, ?, ?, ?)
                """,
                (
                    str(person.id),
                    person.name,
                    person.address,
                    1 if person.active else 0,
                ),
            )
            conn.execute(
                """
                DELETE FROM emails WHERE person_id = ?
                """,
                (str(person.id),),
            )
            for email in person.emails:
                conn.execute(
                    """
                    INSERT INTO emails (person_id, email)
                    VALUES (?, ?)
                    """,
                    (str(person.id), email),
                )

    def list_all(self) -> list[Person]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, name, address, active FROM people"
            ).fetchall()
        return [self.row_to_person(row) for row in rows]

    def remove(self, person_id: PersonId) -> None:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM people WHERE id = ?", (str(person_id),))
            if cursor.rowcount == 0:
                raise PersonNotFound(person_id)

    def get_by_id(self, person_id: PersonId) -> Person | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, name, address, active FROM people WHERE id = ?",
                (str(person_id),),
            ).fetchone()
        if row is None:
            return None
        return self.row_to_person(row)

    def update(
        self,
        person_id: PersonId,
        *,
        name: str | None = None,
        address: str | None = None,
        active: bool | None = None,
        emails: tuple[str, ...] | None = None,
    ) -> Person:
        person = self.get_by_id(person_id)
        if person is None:
            raise PersonNotFound(person_id)

        updated_person = Person(
            id=person.id,
            name=name if name is not None else person.name,
            address=address if address is not None else person.address,
            active=active if active is not None else person.active,
            emails=emails if emails is not None else person.emails,
        )
        # En SQL, update se fait en place: pas d'INSERT ici pour éviter
        # les collisions de clé primaire.
        with self._connect() as conn:
            cursor = conn.execute(
                """
                UPDATE people
                SET name = ?, address = ?, active = ?
                WHERE id = ?
                """,
                (
                    updated_person.name,
                    updated_person.address,
                    1 if updated_person.active else 0,
                    str(updated_person.id),
                ),
            )
            if cursor.rowcount == 0:
                raise PersonNotFound(person_id)
            conn.execute(
                """
                DELETE FROM emails WHERE person_id = ?
                """,
                (str(updated_person.id),),
            )
            for email in updated_person.emails:
                conn.execute(
                    """
                    INSERT INTO emails (person_id, email)
                    VALUES (?, ?)
                    """,
                    (str(updated_person.id), email),
                )
        return updated_person

    def find(
        self,
        *,
        name: str | None = None,
        address: str | None = None,
        active: bool | None = None,
        email: str | None = None,
    ) -> list[Person]:
        # Construction dynamique de la clause WHERE selon les critères fournis.
        query = "SELECT id, name, address, active FROM people"
        conditions = []
        params = []

        if name is not None:
            conditions.append("name = ?")
            params.append(name)
        if address is not None:
            conditions.append("address = ?")
            params.append(address)
        if active is not None:
            conditions.append("active = ?")
            params.append(1 if active else 0)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        with self._connect() as conn:
            rows = conn.execute(query, tuple(params)).fetchall()

        people = [self.row_to_person(row) for row in rows]

        if email is not None:
            people = [p for p in people if email in p.emails]

        return people
