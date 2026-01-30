# tests/test_csv_repository.py
from __future__ import annotations

import pytest

from journey_to_python.domain import Person, PersonId, PersonNotFound
from journey_to_python.infrastructure.csv_repository import CsvPeopleRepository


def test_add_and_list_all_roundtrip(tmp_path) -> None:
    csv_file = tmp_path / "people.csv"
    repo = CsvPeopleRepository(str(csv_file))

    p1 = Person(
        PersonId("ABCDEFGHIJKL"), "John", "13 Main St", True, ("a@b.com", "c@d.com")
    )
    p2 = Person(PersonId("MNOPQRSTUVWX"), "Jane", "42 Side St", False, ())

    repo.add(p1)
    repo.add(p2)

    people = repo.list_all()
    assert [p.id for p in people] == [p1.id, p2.id]
    assert people[0].emails == ("a@b.com", "c@d.com")
    assert people[1].active is False


def test_remove_existing_person(tmp_path) -> None:
    csv_file = tmp_path / "people.csv"
    repo = CsvPeopleRepository(str(csv_file))

    p1 = Person(PersonId("AAAAAAAAAAAA"), "Alice", "Rue 1", True, ())
    p2 = Person(PersonId("BBBBBBBBBBBB"), "Bob", "Rue 2", True, ())

    repo.add(p1)
    repo.add(p2)

    repo.remove(PersonId("AAAAAAAAAAAA"))

    people = repo.list_all()
    assert [p.id for p in people] == [PersonId("BBBBBBBBBBBB")]


def test_remove_missing_raises(tmp_path) -> None:
    csv_file = tmp_path / "people.csv"
    repo = CsvPeopleRepository(str(csv_file))

    repo.add(Person(PersonId("AAAAAAAAAAAA"), "Alice", "Rue 1", True, ()))

    with pytest.raises(PersonNotFound) as exc:
        repo.remove(PersonId("ZZZZZZZZZZZZ"))

    assert exc.value.person_id == PersonId("ZZZZZZZZZZZZ")
