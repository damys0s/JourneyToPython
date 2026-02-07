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


def test_update_full_existing_person(tmp_path) -> None:
    # Arrange: on prépare un CSV temporaire + une personne existante.
    # tmp_path est fourni par pytest et garantit un dossier isolé pour ce test.
    csv_file = tmp_path / "people.csv"
    repo = CsvPeopleRepository(str(csv_file))

    p1 = Person(PersonId("AAAAAAAAAAAA"), "Alice", "Rue 1", True, ())
    repo.add(p1)

    # Act: on met à jour TOUS les champs modifiables de la personne.
    updated = repo.update(
        PersonId("AAAAAAAAAAAA"),
        name="Alice Updated",
        address="New Address",
        active=False,
        emails=("alice.updated@example.com",),
    )

    # Assert: on vérifie que l'objet retourné contient bien les nouvelles valeurs.
    assert updated.id == PersonId("AAAAAAAAAAAA")
    assert updated.name == "Alice Updated"
    assert updated.address == "New Address"
    assert updated.active is False
    assert updated.emails == ("alice.updated@example.com",)


def test_update_missing_person_raises(tmp_path) -> None:
    # Arrange: repo vide => l'ID recherché n'existe pas.
    csv_file = tmp_path / "people.csv"
    repo = CsvPeopleRepository(str(csv_file))

    # Act + Assert erreur:
    # `with pytest.raises(...)` signifie:
    # "le code à l'intérieur DOIT lever PersonNotFound".
    # Si aucune exception n'est levée, le test échoue.
    with pytest.raises(PersonNotFound) as exc:
        repo.update(
            PersonId("ZZZZZZZZZZZZ"),
            name="Nonexistent",
            address="Nowhere",
            active=False,
            emails=(),
        )

    # Assert complémentaire: on valide que l'erreur porte le bon person_id.
    assert exc.value.person_id == PersonId("ZZZZZZZZZZZZ")


def test_update_partial_existing_person(tmp_path) -> None:
    # Arrange: une personne existe déjà en base CSV.
    csv_file = tmp_path / "people.csv"
    repo = CsvPeopleRepository(str(csv_file))

    p1 = Person(PersonId("AAAAAAAAAAAA"), "Alice", "Rue 1", True, ())
    repo.add(p1)

    # Act: update partiel.
    # Convention dans ce projet: un champ à None => on ne le modifie pas.
    updated = repo.update(
        PersonId("AAAAAAAAAAAA"),
        name=None,
        address="New Address",
        active=None,
        emails=None,
    )

    # Assert: seul `address` change; le reste doit rester identique.
    assert updated.id == PersonId("AAAAAAAAAAAA")
    assert updated.name == "Alice"  # inchangé
    assert updated.address == "New Address"  # mis à jour
    assert updated.active is True  # inchangé
    assert updated.emails == ()  # inchangé
