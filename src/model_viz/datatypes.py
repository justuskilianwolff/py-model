from __future__ import annotations

from dataclasses import dataclass


class DataType:
    pass


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
    def __init__(self, inner_dtypes: list[DataType | str] | None = None) -> None:
        self.inner_dtypes = inner_dtypes

    def __str__(self) -> str:
        container = self.__class__.__name__.lower()
        if self.inner_dtypes is None:
            return container
        else:
            return f'{container}[{", ".join(str(dtype) for dtype in self.inner_dtypes)}]'


@dataclass
class Tuple(DataType, Sequence):
    def __init__(self, inner_dtypes: list[DataType | str] | None = None) -> None:
        super().__init__(inner_dtypes)


class List(DataType, Sequence):
    def __init__(self, inner_dtypes: list[DataType | str] | None = None) -> None:
        super().__init__(inner_dtypes)


class Enumeration(DataType):
    def __str__(self) -> str:
        return "Enum"
