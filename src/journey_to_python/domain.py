# src/journey_to_python/domain.py
from __future__ import annotations

import random
import string
from dataclasses import dataclass
from typing import NewType

# NewType crée un "alias typé".
# - À l'exécution : PersonId(3) == 3 (c'est un int normal)
# - Pour les outils de typage : PersonId est un type distinct de int.
# But: éviter de confondre un identifiant (id) avec n'importe quel autre
# int (âge, index, etc.).
PersonId = NewType("PersonId", str)


class DomainError(Exception):
    """
    Erreur "métier" (domain).
    Avantage: tu peux attraper toutes les erreurs métier avec:
        except DomainError:
    sans attraper des erreurs techniques (IOError, ValueError...) par erreur.
    """


class PersonNotFound(DomainError):
    """
    Erreur métier: on a demandé une personne inexistante (id introuvable).
    """

    def __init__(self, person_id: PersonId) -> None:
        # super().__init__(...) appelle le constructeur de Exception
        # et enregistre le message d'erreur.
        super().__init__(f"Person not found: id={str(person_id)}")
        # On garde l'info en attribut pour faciliter tests/logging/debug.
        self.person_id = person_id


@dataclass(frozen=True, slots=True)
class Person:
    """
    Entité métier Person.

    frozen=True : immuable => plus fiable (moins d'effets de bord)
    slots=True  : empêche de créer des attributs "par erreur" et peut économiser
    de la mémoire.

    Note: emails est un tuple pour rester cohérent avec l'immuabilité (tuple immuable).
    """

    id: PersonId
    name: str
    address: str
    active: bool
    emails: tuple[str, ...] = ()

    # src/journey_to_python/domain.py (ou utils.py si tu préfères)


def generate_person_id() -> PersonId:
    """
    Génère un identifiant aléatoire de 12 lettres majuscules.
    Ex: 'ABZQKLMNOPTR'
    """
    return PersonId("".join(random.choices(string.ascii_uppercase, k=12)))
