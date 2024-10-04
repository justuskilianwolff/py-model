from abc import ABC

from py_model.datatypes.basic_types import DataType, Undefined


class TypeHintableValue(ABC):
    """A class that can be used to represent a value that has a type hint, like an attribute or a parameter."""

    def __init__(self, name: str, dtype: DataType) -> None:
        self.name = name
        self.dtype = dtype

    def __str__(self) -> str:
        if isinstance(self.dtype, Undefined):
            # if not defined, we only return the name
            return f"{self.name}"
        else:
            # if defined, we return the name and the type
            return f"{self.name}: {self.dtype}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.name == other.name) and (self.dtype == other.dtype)
