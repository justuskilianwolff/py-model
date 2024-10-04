from abc import ABC

from py_model.datatypes import DataType, Undefined


class TypeHintableValue(ABC):
    def __init__(self, name: str, dtype: DataType) -> None:
        self.name = name
        self.dtype = dtype

    def __str__(self) -> str:
        if isinstance(self.dtype, Undefined):
            return f"{self.name}"
        else:
            return f"{self.name}: {self.dtype}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.name == other.name) and (self.dtype.__class__ == other.dtype.__class__)
