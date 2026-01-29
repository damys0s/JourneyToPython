import random
import string

# dataclass permet de définir des classes de données simplement :
# - génère automatiquement __init__, __repr__, __eq__, etc.
# - réduit énormément le code "boilerplate"
from dataclasses import dataclass, field


def generate_id() -> str:
    # Fonction utilitaire qui génère un identifiant aléatoire composé de
    # 12 lettres majuscules (A–Z).
    #
    # random.choices(...) :
    # - choisit aléatoirement des éléments
    # - k=12 => longueur de l'identifiant
    #
    # ''.join(...) :
    # - assemble la liste de caractères en une seule chaîne
    return "".join(random.choices(string.ascii_uppercase, k=12))


@dataclass
class Person:
    name: str
    address: str
    active: bool = True

    # On utilise default_factory=list et NON pas email_addresses: list[str] = []
    # pour éviter de partager la même liste entre toutes les instances.
    email_adresses: list[str] = field(default_factory=list)

    # default_factory=generate_id :
    # - appelle la fonction generate_id() à la création de l'objet
    # - garantit un ID différent pour chaque instance
    id: str = field(default_factory=generate_id)
