from __future__ import annotations

from typing import Any


class DataType:
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DataType):
            return NotImplemented
        return self.__class__ is other.__class__

    def __repr__(self) -> str:
        # for debugging
        return self.__str__()


class CustomClass(DataType):
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Any):
        if not isinstance(other, CustomClass):
            return NotImplemented
        return self.name == other.name


class Undefined(DataType):
    def __str__(self) -> str:
        return ""


class NoneType(DataType):
    def __str__(self) -> str:
        return "None"


class Integer(DataType):
    def __str__(self) -> str:
        return "int"


class Boolean(DataType):
    def __str__(self) -> str:
        return "bool"


class Float(DataType):
    def __str__(self) -> str:
        return "float"


class String(DataType):
    def __str__(self) -> str:
        return "string"


class Sequence:
    def __init__(self, inner_dtypes: list[DataType] | None = None) -> None:
        self.inner_dtypes = inner_dtypes

    def __str__(self) -> str:
        container = self.__class__.__name__.lower()
        if self.inner_dtypes is None:
            return container
        else:
            return f'{container}[{", ".join(str(dtype) for dtype in self.inner_dtypes)}]'


class NotEmptySequence(Sequence):
    def __init__(self, inner_dtypes: list[DataType | str]) -> None:
        self.inner_dtypes = inner_dtypes


class Tuple(DataType, Sequence):
    def __init__(self, inner_dtypes: list[DataType] | None = None) -> None:
        super().__init__(inner_dtypes)


class List(DataType, Sequence):
    def __init__(self, inner_dtypes: list[DataType] | None = None) -> None:
        super().__init__(inner_dtypes)


class Enumeration(DataType):
    def __str__(self) -> str:
        return "Enum"


class Union(NotEmptySequence, DataType):
    def __init__(self, inner_dtypes: list[DataType | str]) -> None:
        super().__init__(inner_dtypes)

    def __str__(self) -> str:
        return f"{' | '.join(str(dtype) for dtype in self.inner_dtypes)}"
