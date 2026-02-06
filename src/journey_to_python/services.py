# src/journey_to_python/services.py
from .domain import Person, PersonId, PersonNotFound, generate_person_id
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


def update_person(repo: PeopleRepository, *, person_id: PersonId) -> None:
    person = repo.get_by_id(person_id)
    if not person:
        raise PersonNotFound(person_id)
    # On demande à l'utilisateur les champs à mettre à jour (ex: via input()).
    # Pour simplifier, on va juste demander un nouveau nom et adresse.
    repo.update(
        person_id,
        name=person.name,
        address=person.address,
        active=person.active,
        emails=person.emails,
    )
