# src/journey_to_python/repositories.py
from __future__ import annotations

from typing import Protocol

from .domain import Person, PersonId


class PeopleRepository(Protocol):
    """
    Contrat (interface) de persistance.

    IMPORTANT:
    - Un Protocol ne contient pas d'implémentation: il décrit la "forme" attendue.
    - Les "..." indiquent: "méthode à implémenter ailleurs".
    - Ça permet de brancher CSV, SQLite, API, mémoire, etc. sans changer les services.
    """

    def add(self, person: Person) -> None:
        """Persist/ajoute la personne."""
        ...

    def list_all(self) -> list[Person]:
        """Retourne toutes les personnes."""
        ...

    def remove(self, person_id: PersonId) -> None:
        """
        Supprime une personne.

        Version "pro": si l'id n'existe pas, on lève PersonNotFound.
        La CLI peut alors afficher un message clair.
        """
        ...

    def get_by_id(self, person_id: PersonId) -> Person | None:
        """Retourne une personne par son ID, ou None si elle n'existe pas."""
        ...

    def update(
        self,
        person_id: PersonId,
        *,
        name: str | None = None,
        address: str | None = None,
        active: bool | None = None,
        emails: tuple[str, ...] | None = None,
    ) -> Person: ...

    def find(
        self,
        *,
        name: str | None = None,
        address: str | None = None,
        active: bool | None = None,
        email: str | None = None,
    ) -> list[Person]:
        """
        Recherche multi-critères.

        Convention: chaque critère à None signifie "ne pas filtrer ce champ".
        """
        ...
