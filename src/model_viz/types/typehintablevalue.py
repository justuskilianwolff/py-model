from abc import ABC

from model_viz.datatypes import DataType, Undefined


class TypeHintableValue(ABC):
    def __init__(self, name: str, type: DataType) -> None:
        self.name = name
        self.type = type

    def __str__(self) -> str:
        if isinstance(self.type, Undefined):
            return f"{self.name}"
        else:
            return f"{self.name}: {self.type}"
