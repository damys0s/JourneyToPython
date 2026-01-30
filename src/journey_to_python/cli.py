# src/journey_to_python/cli.py
import argparse

from journey_to_python.domain import PersonId, PersonNotFound
from journey_to_python.infrastructure.csv_repository import CsvPeopleRepository
from journey_to_python.services import create_person, list_people, remove_person


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="journey-to-python",
        description="JourneyToPython CLI",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Command: person (create) ---
    person_parser = subparsers.add_parser("person", help="Create a person")
    person_parser.add_argument("--name", required=True, help="Person name")
    person_parser.add_argument("--address", required=True, help="Person address")

    # action="append" permet de répéter --email plusieurs fois:
    # --email a@x.com --email b@y.com
    person_parser.add_argument(
        "--email", action="append", default=[], help="Person email"
    )

    person_parser.add_argument(
        "--inactive", action="store_true", help="Create an inactive person"
    )
    person_parser.add_argument(
        "--csv", default="people.csv", help="Path to the CSV file, default: people.csv"
    )

    # --- Command: list ---
    list_parser = subparsers.add_parser("list", help="List people from CSV")
    list_parser.add_argument(
        "--csv", default="people.csv", help="Path to the CSV file (default: people.csv)"
    )

    # --- Command: remove ---
    remove_parser = subparsers.add_parser(
        "remove", help="Remove a person by ID from CSV"
    )
    remove_parser.add_argument("--id", required=True, help="Remove a person by ID")
    remove_parser.add_argument(
        "--csv", default="people.csv", help="Path to the CSV file (default: people.csv)"
    )

    return parser


def handle_args(args: argparse.Namespace) -> None:
    """
    La CLI doit rester "fine":
    - elle traduit les args en appels de services
    - elle gère l'affichage utilisateur
    - elle n'implémente pas la persistance
    """
    # Chaque commande instancie un repo (CSV ici).
    # Plus tard, tu pourras remplacer CsvPeopleRepository par SQLitePeopleRepository
    # sans changer les services.
    repo = CsvPeopleRepository(args.csv)

    if args.command == "person":
        person = create_person(
            repo,
            name=args.name,
            address=args.address,
            active=not args.inactive,
            emails=args.email,
        )
        print(person)
        print(f"Saved to {args.csv}")
        return

    if args.command == "list":
        people = list_people(repo)
        if not people:
            print(f"No people found in {args.csv}")
            return

        for p in people:
            print(p)
        return

    if args.command == "remove":
        try:
            remove_person(repo, person_id=PersonId(args.id))
        except PersonNotFound as e:
            print(e)
            return

        print(f"Removed person with id={args.id}")
