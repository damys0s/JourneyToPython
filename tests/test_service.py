# tests/test_services.py
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


def test_create_person_adds_person_and_returns_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = FakeRepo()

    # On évite l’aléatoire dans un test: on force l'id généré.
    # Adapte le chemin si tu as mis generate_person_id ailleurs.
    from journey_to_python import services as services_module

    monkeypatch.setattr(
        services_module, "generate_person_id", lambda: PersonId("TESTIDABCDEF")
    )

    person = create_person(
        repo,
        name="John",
        address="13 Main St",
        active=True,
        emails=["a@b.com", "c@d.com"],
    )

    assert person.id == PersonId("TESTIDABCDEF")
    assert person.name == "John"
    assert person.active is True
    assert repo.list_all() == [person]


def test_list_people_returns_all_people() -> None:
    repo = FakeRepo()
    repo.add(Person(PersonId("A"), "Alice", "Rue 1", True, ("a@x.com",)))
    repo.add(Person(PersonId("B"), "Bob", "Rue 2", False, ()))

    people = list_people(repo)

    assert [p.id for p in people] == [PersonId("A"), PersonId("B")]


def test_remove_person_raises_when_missing() -> None:
    repo = FakeRepo()
    repo.add(Person(PersonId("A"), "Alice", "Rue 1", True, ()))

    with pytest.raises(PersonNotFound) as exc:
        remove_person(repo, person_id=PersonId("Z"))

    assert exc.value.person_id == PersonId("Z")


def test_remove_person_removes_when_present() -> None:
    repo = FakeRepo()
    repo.add(Person(PersonId("A"), "Alice", "Rue 1", True, ()))
    repo.add(Person(PersonId("B"), "Bob", "Rue 2", True, ()))

    remove_person(repo, person_id=PersonId("A"))

    assert [p.id for p in repo.list_all()] == [PersonId("B")]
