# tests/test_smoke.py
from journey_to_python.app import main
from journey_to_python.domain import Person, PersonId
from journey_to_python.infrastructure.csv_repository import CsvPeopleRepository


def test_smoke_list(tmp_path, capsys):
    # Arrange: on prépare un chemin CSV isolé (tmp_path est propre à ce test).
    csv_path = tmp_path / "people.csv"

    # Act: on appelle la CLI "list" sans données préexistantes.
    code = main(["list", "--csv", str(csv_path)])
    out = capsys.readouterr()

    # Assert: l'application ne plante pas et informe que la liste est vide.
    assert code == 0
    assert "No people found" in out.out


def test_cli_update_success(tmp_path, capsys):
    # Arrange: on crée un CSV avec une personne existante à mettre à jour.
    csv_path = tmp_path / "people.csv"
    repo = CsvPeopleRepository(str(csv_path))
    repo.add(Person(PersonId("AAAAAAAAAAAA"), "Alice", "Rue 1", True, ()))

    # Act: update partiel via la CLI (ici, uniquement l'adresse).
    code = main(
        [
            "update",
            "--id",
            "AAAAAAAAAAAA",
            "--address",
            "Rue 99",
            "--csv",
            str(csv_path),
        ]
    )
    out = capsys.readouterr()

    # Assert: message de succès + persistance effective dans le CSV.
    assert code == 0
    assert "Updated person with id=AAAAAAAAAAAA" in out.out

    saved = repo.get_by_id(PersonId("AAAAAAAAAAAA"))
    assert saved is not None
    assert saved.address == "Rue 99"


def test_cli_update_missing_fields(tmp_path, capsys):
    # Arrange: une personne existe, mais on appelle update sans champ à modifier.
    csv_path = tmp_path / "people.csv"
    repo = CsvPeopleRepository(str(csv_path))
    repo.add(Person(PersonId("AAAAAAAAAAAA"), "Alice", "Rue 1", True, ()))

    # Act: update avec seulement l'ID (aucune donnée métier fournie).
    code = main(["update", "--id", "AAAAAAAAAAAA", "--csv", str(csv_path)])
    out = capsys.readouterr()

    # Assert: la CLI retourne 0 mais affiche l'erreur métier attendue.
    assert code == 0
    assert "No fields to update for person id=AAAAAAAAAAAA" in out.out


def test_cli_update_conflicting_active_flags(tmp_path, capsys):
    # Arrange: personne existante.
    csv_path = tmp_path / "people.csv"
    repo = CsvPeopleRepository(str(csv_path))
    repo.add(Person(PersonId("AAAAAAAAAAAA"), "Alice", "Rue 1", True, ()))

    # Act: on passe --active et --inactive en même temps (cas invalide).
    code = main(
        [
            "update",
            "--id",
            "AAAAAAAAAAAA",
            "--active",
            "--inactive",
            "--csv",
            str(csv_path),
        ]
    )
    out = capsys.readouterr()

    # Assert: message de validation clair.
    assert code == 0
    assert "Cannot set both --active and --inactive" in out.out


def test_cli_update_missing_person(tmp_path, capsys):
    # Arrange: CSV vide => l'ID demandé n'existe pas.
    csv_path = tmp_path / "people.csv"

    # Act: tentative d'update sur un ID absent.
    code = main(
        [
            "update",
            "--id",
            "ZZZZZZZZZZZZ",
            "--name",
            "Ghost",
            "--csv",
            str(csv_path),
        ]
    )
    out = capsys.readouterr()

    # Assert: la CLI expose le message PersonNotFound.
    assert code == 0
    assert "Person not found: id=ZZZZZZZZZZZZ" in out.out
