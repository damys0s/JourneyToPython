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

    def next_id(self) -> PersonId:
        """Retourne un nouvel identifiant unique."""
        ...

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
