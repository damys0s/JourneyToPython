# src/journey_to_python/cli.py

# Module standard Python pour construire des interfaces en ligne de commande (CLI)
# - gère automatiquement --help, la validation des arguments, les erreurs, etc.
import argparse

# On importe le modèle "métier" (logique de données) : la CLI ne réinvente pas Person,
# elle se contente de le piloter via des arguments.
from journey_to_python.models.person import Person
from journey_to_python.storage.csv_store import (
    append_person,
    read_people,
    remove_person_by_id,
)


def build_parser() -> argparse.ArgumentParser:
    # Cette fonction "décrit" la CLI (commandes + arguments).
    # Elle ne lit pas encore ce que l'utilisateur tape, elle construit juste le parseur.
    parser = argparse.ArgumentParser(
        # Nom affiché dans l'aide (utile si tu renommes le script/commande)
        prog="journey-to-python",
        # Description affichée en haut de `--help`
        description="JourneyToPython CLI",
    )

    # On crée un système de sous-commandes (ex: `journey-to-python person ...`).
    # - dest="command" : le nom de la sous-commande choisie sera dans args.command
    # - required=True : l'utilisateur doit choisir une sous-commande
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Déclare la sous-commande "person"
    # Elle sera appelée comme : `journey-to-python person ...`
    person_parser = subparsers.add_parser("person", help="Create a person")

    # Ajoute l'argument --name (obligatoire)
    # Exemple : `--name John`
    person_parser.add_argument("--name", required=True, help="Person name")

    # Ajoute l'argument --address (obligatoire)
    # Exemple : `--address "13 Main St"`
    person_parser.add_argument("--address", required=True, help="Person address")

    person_parser.add_argument(
        "--email", action="append", default=[], help="Person email"
    )

    # Ajoute un drapeau booléen : --inactive
    # - absent => args.inactive == False
    # - présent => args.inactive == True
    person_parser.add_argument(
        "--inactive", action="store_true", help="Create an inactive person"
    )

    # Ajoute l'argument --csv (optionnel, avec valeur par défaut)
    # Exemple : `--csv people.csv`
    person_parser.add_argument(
        "--csv",
        default="people.csv",
        help="Path to the CSV file, default: people.csv",
    )

    list_parser = subparsers.add_parser("list", help="List people from CSV")
    list_parser.add_argument(
        "--csv",
        default="people.csv",
        help="Path to the CSV file (default: people.csv)",
    )
    remove_parser = subparsers.add_parser(
        "remove", help="Remove a person by ID from CSV"
    )
    remove_parser.add_argument(
        "--id",
        required=True,
        help="Remove a person by ID",
    )
    remove_parser.add_argument(
        "--csv",
        default="people.csv",
        help="Path to the CSV file (default: people.csv)",
    )

    # On renvoie le parseur entièrement configuré.
    return parser


def handle_args(args: argparse.Namespace) -> None:
    # --- Command: person -----------------------------------------------------
    if args.command == "person":
        person = Person(
            name=args.name,
            address=args.address,
            active=not args.inactive,
            email_adresses=args.email,
        )
        print(person)

        append_person(args.csv, person)
        print(f"Saved to {args.csv}")
        return

    # --- Command: list -------------------------------------------------------
    if args.command == "list":
        people = read_people(args.csv)

        if not people:
            print(f"No people found in {args.csv}")
            return

        for p in people:
            print(p)
        return

    # --- Command: remove -----------------------------------------------------
    if args.command == "remove":
        removed = remove_person_by_id(args.csv, args.id)

        if removed:
            print(f"Removed person with id={args.id} from {args.csv}")
        else:
            print(f"No person found with id={args.id} in {args.csv}")
        return
