# tests/test_service.py
from __future__ import annotations

import pytest

from journey_to_python.domain import Person, PersonId, PersonNotFound
from journey_to_python.services import create_person, list_people, remove_person


class FakeRepo:
    """
    Repository en mémoire pour tester les services sans dépendre du CSV.
    Ici on simule le comportement attendu du repository.
    """

    def __init__(self) -> None:
        self._people: list[Person] = []

    def add(self, person: Person) -> None:
        self._people.append(person)

    def list_all(self) -> list[Person]:
        return list(self._people)

    def remove(self, person_id: PersonId) -> None:
        before = len(self._people)
        self._people = [p for p in self._people if p.id != person_id]
        if len(self._people) == before:
            raise PersonNotFound(person_id)

    def get_by_id(self, person_id: PersonId) -> Person | None:
        for p in self._people:
            if p.id == person_id:
                return p
        return None

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

        updated = Person(
            id=person.id,
            name=name if name is not None else person.name,
            address=address if address is not None else person.address,
            active=active if active is not None else person.active,
            emails=emails if emails is not None else person.emails,
        )
        self._people = [p for p in self._people if p.id != person_id] + [updated]
        return updated


def test_create_person_adds_person_and_returns_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange: repo en mémoire + ID déterministe (on retire l'aléatoire pour un test
    # stable).
    repo = FakeRepo()
    from journey_to_python import services as services_module

    monkeypatch.setattr(
        services_module, "generate_person_id", lambda: PersonId("TESTIDABCDEF")
    )

    # Act: appel du service de création.
    person = create_person(
        repo,
        name="John",
        address="13 Main St",
        active=True,
        emails=("a@b.com", "c@d.com"),
    )

    # Assert: la personne renvoyée et la persistance en repo sont correctes.
    assert person.id == PersonId("TESTIDABCDEF")
    assert person.name == "John"
    assert person.active is True
    assert repo.list_all() == [person]


def test_list_people_returns_all_people() -> None:
    # Arrange: deux personnes déjà présentes dans le fake repo.
    repo = FakeRepo()
    repo.add(Person(PersonId("A"), "Alice", "Rue 1", True, ("a@x.com",)))
    repo.add(Person(PersonId("B"), "Bob", "Rue 2", False, ()))

    # Act: on demande la liste via le service.
    people = list_people(repo)

    # Assert: on récupère bien les deux IDs dans l'ordre attendu.
    assert [p.id for p in people] == [PersonId("A"), PersonId("B")]


def test_remove_person_raises_when_missing() -> None:
    # Arrange: repo avec une seule personne, différente de l'ID ciblé.
    repo = FakeRepo()
    repo.add(Person(PersonId("A"), "Alice", "Rue 1", True, ()))

    # Act + Assert erreur:
    # Le bloc `with pytest.raises(...)` vérifie que l'exception est bien levée.
    with pytest.raises(PersonNotFound) as exc:
        remove_person(repo, person_id=PersonId("Z"))

    # Assert complémentaire: l'exception contient le bon ID.
    assert exc.value.person_id == PersonId("Z")


def test_remove_person_removes_when_present() -> None:
    # Arrange: deux personnes en repo.
    repo = FakeRepo()
    repo.add(Person(PersonId("A"), "Alice", "Rue 1", True, ()))
    repo.add(Person(PersonId("B"), "Bob", "Rue 2", True, ()))

    # Act: suppression de la personne A.
    remove_person(repo, person_id=PersonId("A"))

    # Assert: seule la personne B reste en mémoire.
    assert [p.id for p in repo.list_all()] == [PersonId("B")]


def test_validate_email_raises_on_invalid_email() -> None:
    from journey_to_python.services import InvalidEmail, validate_email

    with pytest.raises(InvalidEmail) as exc:
        validate_email("invalid-email")

    assert exc.value.email == "invalid-email"

    with pytest.raises(InvalidEmail) as exc:
        validate_email("")

    assert exc.value.email == ""

    with pytest.raises(InvalidEmail) as exc:
        validate_email("user@domain")

    assert exc.value.email == "user@domain"


def test_validate_email_accepts_valid_email() -> None:
    from journey_to_python.services import validate_email

    valid_email = "user@example.com"
    assert validate_email(valid_email) == valid_email


def test_validate_emails_raises_on_invalid_email_in_list() -> None:
    from journey_to_python.services import InvalidEmail, validate_emails

    with pytest.raises(InvalidEmail) as exc:
        validate_emails(("valid@example.com", "invalid-email"))

    assert exc.value.email == "invalid-email"


def test_validate_emails_accepts_all_valid_emails() -> None:
    from journey_to_python.services import validate_emails

    valid_emails = ("user1@example.com", "user2@example.com")
    assert validate_emails(valid_emails) == valid_emails


def test_validate_name_raises_on_empty_name() -> None:
    from journey_to_python.services import InvalidPersonData, validate_name

    with pytest.raises(InvalidPersonData) as exc:
        validate_name("")

    assert exc.value.message == "Name cannot be empty"


def test_validate_name_accepts_valid_name() -> None:
    from journey_to_python.services import validate_name

    valid_name = "Alice"
    assert validate_name(valid_name) == valid_name


def test_get_person_returns_person_when_exists() -> None:
    repo = FakeRepo()
    person = Person(PersonId("A"), "Alice", "Rue 1", True, ())
    repo.add(person)

    from journey_to_python.services import get_person

    result = get_person(repo, person_id=PersonId("A"))
    assert result == person


def test_get_person_raises_when_not_found() -> None:
    repo = FakeRepo()

    from journey_to_python.services import PersonNotFound, get_person

    with pytest.raises(PersonNotFound) as exc:
        get_person(repo, person_id=PersonId("Z"))

    assert exc.value.person_id == PersonId("Z")
