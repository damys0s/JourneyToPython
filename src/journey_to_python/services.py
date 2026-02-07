# src/journey_to_python/services.py
from .domain import (
    InvalidEmail,
    InvalidPersonData,
    Person,
    PersonId,
    PersonUpdateEmpty,
    generate_person_id,
)
from .repositories import PeopleRepository


def create_person(
    repo: PeopleRepository,
    *,
    name: str,
    address: str,
    active: bool,
    emails: list[str],
) -> Person:
    person = Person(
        id=generate_person_id(),
        name=validate_name(name),
        address=address,
        active=active,
        emails=validate_emails(emails),
    )
    repo.add(person)
    return person


def list_people(repo: PeopleRepository) -> list[Person]:
    return repo.list_all()


def remove_person(repo: PeopleRepository, *, person_id: PersonId) -> None:
    repo.remove(person_id)


def update_person(
    repo: PeopleRepository,
    *,
    person_id: PersonId,
    name: str | None = None,
    address: str | None = None,
    active: bool | None = None,
    emails: tuple[str, ...] | None = None,
) -> Person:
    if name is None and address is None and active is None and emails is None:
        raise PersonUpdateEmpty(person_id)

    return repo.update(
        person_id,
        name=validate_name(name) if name is not None else None,
        address=address,
        active=active,
        emails=validate_emails(emails) if emails is not None else None,
    )


def validate_email(email: str) -> str:
    """
    Valide l'adresse email selon des règles simples (ex: doit contenir '@').

    Lève InvalidEmail si l'email est invalide.

    """
    if "@" not in email:
        raise InvalidEmail(email)
    if email.strip() == "":
        raise InvalidEmail(email)
    local, domain = email.split("@", 1)
    if "." not in domain:
        raise InvalidEmail(email)
    return email


def validate_emails(emails: tuple[str, ...]) -> tuple[str, ...]:
    """
    Valide une liste d'emails et retourne un tuple d'emails valides.

    Lève InvalidEmail si au moins un email est invalide.
    """
    valid_emails = []
    for email in emails:
        valid_emails.append(validate_email(email))
    return tuple(valid_emails)


def validate_name(name: str) -> str:
    """
    Valide le nom d'une personne (ex: ne doit pas être vide).

    Lève ValueError si le nom est invalide.
    """
    if name.strip() == "":
        raise InvalidPersonData("Name cannot be empty")
    return name
