# src/journey_to_python/app.py

# app.py joue le rôle de "chef d'orchestre" :
# - il ne contient pas la logique métier (ça, c'est dans models/)
# - il ne détaille pas toute la définition de la CLI (ça, c'est dans cli.py)
# Il se contente de :
# 1) construire le parseur
# 2) lire/valider les arguments utilisateur
# 3) déléguer l'exécution de la commande
from journey_to_python.cli import build_parser, handle_args


def main() -> None:
    # Point d'entrée principal de l'application.
    # Cette fonction sera appelée :
    # - via `python -m journey_to_python` (en passant par __main__.py)
    # - via la commande CLI (entrypoint) `journey-to-python` si déclarée dans
    # pyproject.toml

    # 1) On récupère un parseur CLI déjà configuré (commandes + arguments)
    parser = build_parser()

    # 2) On parse les arguments fournis en ligne de commande.
    # argparse :
    # - lit ce que l'utilisateur a tapé
    # - valide les arguments (required, types, etc.)
    # - affiche automatiquement --help si demandé
    # - lève une erreur "user-friendly" si les arguments sont invalides
    args = parser.parse_args()

    # 3) On exécute la logique correspondant à la sous-commande choisie
    handle_args(args)
