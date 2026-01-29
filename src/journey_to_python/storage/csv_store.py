# src/journey_to_python/storage/csv_store.py

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, TypedDict, cast

from journey_to_python.models.person import Person

# Colonnes du CSV (source de vérité unique)
FIELDNAMES: list[str] = ["id", "name", "address", "active", "email_adresses"]


class PersonRow(TypedDict):
    """Représente une ligne CSV (toutes les valeurs sont du texte)."""

    id: str
    name: str
    address: str
    active: str
    email_adresses: str


def person_to_row(person: Person) -> PersonRow:
    """
    Convertit une Person en "ligne CSV" (dictionnaire).
    - CSV = texte => on stocke active en "True"/"False"
    """
    return {
        "id": person.id,
        "name": person.name,
        "address": person.address,
        "active": str(person.active),
        "email_adresses": ";".join(person.email_adresses),
    }


def row_to_person(row: dict[str, str]) -> Person:
    """
    Convertit une ligne CSV (DictReader -> dict[str, str]) en Person.
    Important : on réutilise l'id présent dans le fichier (on ne le régénère pas).
    """
    emails_cell = row.get("email_adresses", "")
    emails = emails_cell.split(";") if emails_cell else []

    return Person(
        id=row["id"],
        name=row["name"],
        address=row["address"],
        active=(row.get("active", "True") == "True"),
        email_adresses=emails,
    )


def ensure_parent_dir(path: Path) -> None:
    """Crée le dossier parent du fichier si nécessaire."""
    path.parent.mkdir(parents=True, exist_ok=True)


def file_is_missing_or_empty(path: Path) -> bool:
    """Retourne True si le fichier n'existe pas ou est vide."""
    return (not path.exists()) or (path.stat().st_size == 0)


def write_people(path: str | Path, people: list[Person]) -> None:
    """
    (Re)écrit entièrement le CSV avec la liste de personnes donnée.
    - Écrit toujours l'en-tête
    - Écrase le fichier existant
    """
    p = Path(path)
    ensure_parent_dir(p)

    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

        for person in people:
            # Pylance : certains stubs csv sont trop stricts
            # on caste pour calmer le typage
            writer.writerow(cast(dict[str, Any], person_to_row(person)))


def append_person(path: str | Path, person: Person) -> None:
    """
    Ajoute une personne à la fin du CSV.
    - Crée le fichier + en-tête si nécessaire
    - N'écrase pas le contenu existant
    """
    p = Path(path)
    ensure_parent_dir(p)

    needs_header = file_is_missing_or_empty(p)

    with p.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if needs_header:
            writer.writeheader()

        writer.writerow(cast(dict[str, Any], person_to_row(person)))


def read_people(path: str | Path) -> list[Person]:
    """
    Lit le CSV et renvoie une liste de Person.
    - Si le fichier n'existe pas ou est vide : renvoie []
    """
    p = Path(path)
    if file_is_missing_or_empty(p):
        return []

    people: list[Person] = []

    with p.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Si le CSV n'a pas d'en-tête correct, DictReader peut renvoyer fieldnames=None
        if reader.fieldnames is None:
            return []

        for row in reader:
            # DictReader renvoie dict[str, str | None] selon les stubs
            # => on normalise en str
            normalized: dict[str, str] = {k: (v or "") for k, v in row.items()}
            people.append(row_to_person(normalized))

    return people


def remove_person_by_id(path: str | Path, person_id: str) -> bool:
    """
    Supprime une personne du CSV par son ID.
    Retourne :
      - True si une personne a été supprimée
      - False si l'ID n'existait pas (ou fichier vide/inexistant)
    """
    people = read_people(path)
    if not people:
        return False

    filtered_people = [p for p in people if p.id != person_id]
    if len(filtered_people) == len(people):
        return False

    write_people(path, filtered_people)
    return True
