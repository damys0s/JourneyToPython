# src/journey_to_python/cli.py
import argparse

from journey_to_python.domain import PersonId, PersonNotFound, PersonUpdateEmpty
from journey_to_python.infrastructure.csv_repository import CsvPeopleRepository
from journey_to_python.infrastructure.sqlite_repository import SQLitePeopleRepository
from journey_to_python.services import (
    create_person,
    find_people,
    get_person,
    list_people,
    remove_person,
    update_person,
)


def build_repo(args):
    # Point de décision unique pour choisir l'infrastructure de persistance.
    if args.backend == "sqlite":
        return SQLitePeopleRepository(args.sqlite)
    return CsvPeopleRepository(args.csv)


def file_save_message_type(args):
    # Utilisé uniquement pour afficher le chemin cible à l'utilisateur.
    if args.backend == "sqlite":
        return f"{args.sqlite}"
    return f"{args.csv}"


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
        "--csv", default="people.csv", help="Path to the CSV file (default: people.csv)"
    )
    person_parser.add_argument(
        "--sqlite",
        default="people.db",
        help="Path to the SQLite file (default: people.db)",
    )
    person_parser.add_argument(
        "--backend",
        choices=["csv", "sqlite"],
        default="csv",
        help="Choose the backend to use (default: csv)",
    )

    # --- Command: list ---
    list_parser = subparsers.add_parser("list", help="List people from CSV")
    list_parser.add_argument(
        "--csv", default="people.csv", help="Path to the CSV file (default: people.csv)"
    )
    list_parser.add_argument(
        "--sqlite",
        default="people.db",
        help="Path to the SQLite file (default: people.db)",
    )
    list_parser.add_argument(
        "--backend",
        choices=["csv", "sqlite"],
        default="csv",
        help="Choose the backend to use (default: csv)",
    )

    # --- Command: remove ---
    remove_parser = subparsers.add_parser(
        "remove", help="Remove a person by ID from CSV"
    )
    remove_parser.add_argument("--id", required=True, help="Remove a person by ID")
    remove_parser.add_argument(
        "--csv", default="people.csv", help="Path to the CSV file (default: people.csv)"
    )
    remove_parser.add_argument(
        "--sqlite",
        default="people.db",
        help="Path to the SQLite file (default: people.db)",
    )
    remove_parser.add_argument(
        "--backend",
        choices=["csv", "sqlite"],
        default="csv",
        help="Choose the backend to use (default: csv)",
    )

    # --- Command: update ---
    update_parser = subparsers.add_parser(
        "update", help="Update a person by ID from CSV"
    )
    update_parser.add_argument("--id", required=True, help="Update a person by ID")
    update_parser.add_argument("--name", required=False, help="Set a person name")
    update_parser.add_argument("--address", required=False, help="Set a person address")
    update_parser.add_argument(
        "--active", action="store_true", help="Set person as active"
    )
    update_parser.add_argument(
        "--inactive", action="store_true", help="Set person as inactive"
    )
    update_parser.add_argument(
        "--email", action="append", default=None, help="Set person email (repeatable)"
    )
    update_parser.add_argument(
        "--csv", default="people.csv", help="Path to the CSV file (default: people.csv)"
    )
    update_parser.add_argument(
        "--sqlite",
        default="people.db",
        help="Path to the SQLite file (default: people.db)",
    )
    update_parser.add_argument(
        "--backend",
        choices=["csv", "sqlite"],
        default="csv",
        help="Choose the backend to use (default: csv)",
    )

    # --- Command: get ---
    get_parser = subparsers.add_parser("get", help="Get a person by ID from CSV")
    get_parser.add_argument("--id", required=True, help="Get a person by ID")
    get_parser.add_argument(
        "--csv", default="people.csv", help="Path to the CSV file (default: people.csv)"
    )
    get_parser.add_argument(
        "--sqlite",
        default="people.db",
        help="Path to the SQLite file (default: people.db)",
    )
    get_parser.add_argument(
        "--backend",
        choices=["csv", "sqlite"],
        default="csv",
        help="Choose the backend to use (default: csv)",
    )

    # -- Command: find people by criteria (name, address, active/inactive, email) ---
    find_parser = subparsers.add_parser("find", help="Find people by criteria")
    find_parser.add_argument("--name", required=False, help="Find by name")
    find_parser.add_argument("--address", required=False, help="Find by address")
    find_parser.add_argument("--active", action="store_true", help="Find active people")
    find_parser.add_argument(
        "--inactive", action="store_true", help="Find inactive people"
    )
    find_parser.add_argument(
        "--email", action="append", default=None, help="Find by email (repeatable)"
    )
    find_parser.add_argument(
        "--csv", default="people.csv", help="Path to the CSV file (default: people.csv)"
    )
    find_parser.add_argument(
        "--sqlite",
        default="people.db",
        help="Path to the SQLite file (default: people.db)",
    )
    find_parser.add_argument(
        "--backend",
        choices=["csv", "sqlite"],
        default="csv",
        help="Choose the backend to use (default: csv)",
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
    repo = build_repo(args)

    if args.command == "person":
        person = create_person(
            repo,
            name=args.name,
            address=args.address,
            active=not args.inactive,
            emails=args.email,
        )
        print(person)
        print("Saved to", file_save_message_type(args), " !")
        return

    if args.command == "list":
        people = list_people(repo)
        if not people:
            print(f"No people found in {file_save_message_type(args)}")
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

        print("Removed from", file_save_message_type(args), " !")

    if args.command == "update":
        if not (
            args.name or args.address or args.active or args.inactive or args.email
        ):
            try:
                raise PersonUpdateEmpty(PersonId(args.id))
            except PersonUpdateEmpty as e:
                print(e)
                return

        if args.active and args.inactive:
            print("Cannot set both --active and --inactive")
            return
        # Tri-state:
        # - True  => force actif
        # - False => force inactif
        # - None  => ne pas modifier l'état actuel
        active_value = True if args.active else False if args.inactive else None

        try:
            update_person(
                repo,
                person_id=PersonId(args.id),
                name=args.name,
                address=args.address,
                active=active_value,
                emails=tuple(args.email) if args.email is not None else None,
            )
        except PersonNotFound as e:
            print(e)
            return

        print(f"Updated person with id={args.id} in {file_save_message_type(args)} !")

    if args.command == "get":
        try:
            person = get_person(repo, person_id=PersonId(args.id))
        except PersonNotFound as e:
            print(e)
            return

        print(person)

    if args.command == "find":
        # Ex: journey-to-python find --name "Alice"
        try:
            people = find_people(
                repo,
                name=args.name,
                address=args.address,
                active=True if args.active else False if args.inactive else None,
                # La CLI accepte --email répétable, mais la recherche actuelle
                # utilise un seul email (le premier) comme critère.
                email=args.email[0] if args.email is not None else None,
            )
        except PersonNotFound:
            print("No people found matching the criteria.")
            return

        for p in people:
            print(p)
