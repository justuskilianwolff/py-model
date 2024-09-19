from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int

    def greet(self) -> None:
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
