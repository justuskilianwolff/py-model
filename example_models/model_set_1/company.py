from dataclasses import dataclass

from .employee import Employee


@dataclass
class Company:
    name: str
    employees: list[Employee]
