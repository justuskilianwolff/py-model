from dataclasses import dataclass

from .person import Person


@dataclass
class Employee(Person):
    id: int
    salary: float
