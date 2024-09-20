from abc import ABC


class TypeHintableValue(ABC):
    def __init__(self, name: str, type: str | None) -> None:
        self.name = name
        self.type = type

    def __str__(self) -> str:
        if self.type is None:
            return f"{self.name}"
        else:
            return f"{self.name}: {self.type}"
