from abc import ABC

from model_viz.datatypes import DataType, Undefined


class TypeHintableValue(ABC):
    def __init__(self, name: str, dtype: DataType) -> None:
        self.name = name
        self.dtype = dtype

    def __str__(self) -> str:
        if isinstance(self.dtype, Undefined):
            return f"{self.name}"
        else:
            return f"{self.name}: {self.dtype}"
