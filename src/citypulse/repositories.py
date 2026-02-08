from __future__ import annotations

from typing import Protocol

from .domain import CityData


class CityPulseRepository(Protocol):
    def get_city_data(self, city: str) -> CityData | None:
        """Retourne les données d'une ville, ou None si introuvable."""
        ...

    def add_city_data(self, city_data: CityData) -> None:
        """Ajoute ou met à jour les données d'une ville."""
        ...

    def update_city_data(self, city_data: CityData) -> None:
        """Met à jour les données d'une ville existante."""
        ...

    def delete_city_data(self, city: str) -> bool:
        """Supprime les données d'une ville. Retourne True si supprimé,
        False si introuvable."""
        ...

    def list_cities(self) -> list[str]:
        """Retourne la liste des villes disponibles."""
        ...
