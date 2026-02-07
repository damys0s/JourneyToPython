# src/journey_to_python/infrastructure/csv_repository.py
from __future__ import annotations

import csv
from dataclasses import dataclass, replace
from pathlib import Path

from journey_to_python.domain import InvalidPersonData, Person, PersonId, PersonNotFound
from journey_to_python.repositories import PeopleRepository


@dataclass
class CsvPeopleRepository(PeopleRepository):
    """
    Implémentation CSV du repository.

    Format CSV (avec en-têtes) :
      id,name,address,active,emails

    - id: string opaque (ex: 'ABZQKLMNOPTR')
    - active: "true"/"false"
    - emails: liste séparée par ';'
    """

    HEADERS = ["id", "name", "address", "active", "emails"]

    def __init__(self, csv_path: str) -> None:
        self.path = Path(csv_path)

    # -------------------------
    # Helpers internes
    # -------------------------
    def _ensure_file_exists(self) -> None:
        """Crée le fichier CSV s'il n'existe pas, avec l'en-tête."""
        if self.path.exists():
            return

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.HEADERS)
            writer.writeheader()

    def _person_to_row(self, person: Person) -> dict[str, str]:
        """Convertit Person -> dict compatible CSV (str->str)."""
        return {
            "id": str(person.id),  # PersonId est un NewType(str) => convertible en str
            "name": person.name,
            "address": person.address,
            "active": "true" if person.active else "false",
            "emails": ";".join(person.emails),
        }

    def _row_to_person(self, row: dict[str, str]) -> Person:
        """Convertit dict CSV -> Person."""
        active_str = (row.get("active") or "").strip().lower()
        active = active_str in ("true", "1", "yes", "y")

        emails_raw = (row.get("emails") or "").strip()
        emails = tuple(e.strip() for e in emails_raw.split(";") if e.strip())

        # id est une string opaque
        pid = PersonId((row.get("id") or "").strip())

        return Person(
            id=pid,
            name=(row.get("name") or "").strip(),
            address=(row.get("address") or "").strip(),
            active=active,
            emails=emails,
        )

    def _rewrite_all(self, people: list[Person]) -> None:
        """
        Réécrit complètement le fichier CSV avec la liste fournie.
        Helper centralisé => pas de duplication de code.

        Note: en CSV, update/delete implique un rewrite complet du fichier.
        """
        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.HEADERS)
            writer.writeheader()
            for p in people:
                writer.writerow(self._person_to_row(p))

    # -------------------------
    # Méthodes du repository
    # -------------------------
    def add(self, person: Person) -> None:
        """Ajoute une personne à la fin du CSV."""
        self._ensure_file_exists()
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.HEADERS)
            writer.writerow(self._person_to_row(person))

    def list_all(self) -> list[Person]:
        """Retourne toutes les personnes du CSV."""
        self._ensure_file_exists()
        with self.path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # ignore les lignes vides / invalides
            return [
                self._row_to_person(row)
                for row in reader
                if (row.get("id") or "").strip()
            ]

    def remove(self, person_id: PersonId) -> None:
        """
        Supprime une personne par id.
        Version pro: lève PersonNotFound si l'id n'existe pas.
        """
        self._ensure_file_exists()
        people = self.list_all()

        remaining = [p for p in people if p.id != person_id]

        if len(remaining) == len(people):
            raise PersonNotFound(person_id)

        self._rewrite_all(remaining)

    def get_by_id(self, person_id: PersonId) -> Person | None:
        """Retourne une personne par son ID, ou None si elle n'existe pas."""
        self._ensure_file_exists()
        people = self.list_all()
        for p in people:
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
        """
        Met à jour une personne.

        Version pro: lève PersonNotFound si l'id n'existe pas.
        """
        self._ensure_file_exists()
        people = self.list_all()

        # Stratégie CSV: lecture complète -> modification en mémoire -> rewrite complet.
        updated = False
        for i, p in enumerate(people):
            if p.id == person_id:
                person = replace(
                    p,
                    name=name if name is not None else p.name,
                    address=address if address is not None else p.address,
                    active=active if active is not None else p.active,
                    emails=emails if emails is not None else p.emails,
                )
                people[i] = person
                updated = True
                break
        else:
            raise PersonNotFound(person_id)

        if not updated:
            raise PersonNotFound(person_id)

        self._rewrite_all(people)
        return people[i]

    def find(
        self,
        *,
        name: str | None = None,
        address: str | None = None,
        active: bool | None = None,
        email: str | None = None,
    ) -> list[Person]:
        """
        Recherche des personnes par critères.

        Tous les critères sont optionnels, mais au moins un doit être fourni.
        Retourne la liste des personnes qui matchent tous les critères fournis.
        """
        if name is None and address is None and active is None and email is None:
            raise InvalidPersonData("At least one search criterion must be provided")

        # Pas d'index en CSV: on fait un filtrage en mémoire.
        people = self.list_all()
        results = []
        for p in people:
            if name is not None and name.lower() not in p.name.lower():
                continue
            if address is not None and address.lower() not in p.address.lower():
                continue
            if active is not None and p.active != active:
                continue
            if email is not None and all(email.lower() != e.lower() for e in p.emails):
                continue
            results.append(p)
        return results
