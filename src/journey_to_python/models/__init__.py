from journey_to_python.models.person import Person


def main() -> None:
    person = Person(name="John", address="13 Main St")
    print(person)
