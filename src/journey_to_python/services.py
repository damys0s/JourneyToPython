# src/journey_to_python/services.py
from .domain import Person, PersonId, generate_person_id
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
        name=name,
        address=address,
        active=active,
        emails=tuple(emails),
    )
    repo.add(person)
    return person


def list_people(repo: PeopleRepository) -> list[Person]:
    return repo.list_all()


def remove_person(repo: PeopleRepository, *, person_id: PersonId) -> None:
    repo.remove(person_id)
