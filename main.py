import random
import string
from dataclasses import dataclass, field


def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=12))


@dataclass
class Person:
    name: str
    address: str
    active: bool = True
    email_adresses: list[str] = field(default_factory=list)
    id: str = field(default_factory=generate_id)


def main() -> None:
    person = Person(name="John", address="13 Main St")
    print(person)


if __name__ == "__main__":
    main()
