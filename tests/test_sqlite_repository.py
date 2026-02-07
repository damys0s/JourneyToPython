from __future__ import annotations

import pytest

from journey_to_python.domain import Person, PersonId, PersonNotFound
from journey_to_python.infrastructure.sqlite_repository import SQLitePeopleRepository


def test_add_and_list_all_roundtrip(tmp_path) -> None:
    db_file = tmp_path / "people.db"
    repo = SQLitePeopleRepository(str(db_file))

    p1 = PersonId("ABCDEFGHIJKL"), "John", "13 Main St", True, ("john@example.com",)
    repo.add(Person(*p1))

    people = repo.list_all()
    assert len(people) == 1
    assert people[0].id == p1[0]
    assert people[0].name == p1[1]
    assert people[0].address == p1[2]
    assert people[0].active == p1[3]
    assert people[0].emails == p1[4]


def test_remove_existing_person(tmp_path) -> None:
    db_file = tmp_path / "people.db"
    repo = SQLitePeopleRepository(str(db_file))

    p1 = PersonId("ABCDEFGHIJKL"), "John", "13 Main St", True, ("john@example.com",)
    repo.add(Person(*p1))
    repo.remove(p1[0])

    people = repo.list_all()
    assert len(people) == 0


def test_remove_missing_raises(tmp_path) -> None:
    db_file = tmp_path / "people.db"
    repo = SQLitePeopleRepository(str(db_file))

    p1 = PersonId("ABCDEFGHIJKL"), "John", "13 Main St", True, ("john@example.com",)
    repo.add(Person(*p1))
    with pytest.raises(PersonNotFound) as exc:
        repo.remove(PersonId("ZZZZZZZZZZZZ"))
    assert exc.value.person_id == PersonId("ZZZZZZZZZZZZ")


def test_update_full_existing_person(tmp_path) -> None:
    db_file = tmp_path / "people.db"
    repo = SQLitePeopleRepository(str(db_file))

    p1 = PersonId("ABCDEFGHIJKL"), "John", "13 Main St", True, ("john@example.com",)
    repo.add(Person(*p1))
    repo.update(
        p1[0],
        name="John Doe",
        address="42 Side St",
        active=False,
        emails=["john.doe@example.com"],
    )
    people = repo.list_all()
    assert len(people) == 1
    assert people[0].name == "John Doe"
    assert people[0].address == "42 Side St"
    assert not people[0].active
    assert people[0].emails == ("john.doe@example.com",)


def test_update_missing_person(tmp_path) -> None:
    db_file = tmp_path / "people.db"
    repo = SQLitePeopleRepository(str(db_file))

    with pytest.raises(PersonNotFound) as exc:
        repo.update(
            PersonId("ZZZZZZZZZZZZ"),
            name="Jane Doe",
            address="99 Unknown St",
            active=True,
            emails=["jane.doe@example.com"],
        )
    assert exc.value.person_id == PersonId("ZZZZZZZZZZZZ")
