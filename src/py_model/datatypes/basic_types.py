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


class Boolean(DataType):
    def __str__(self) -> str:
        return "bool"


class Integer(DataType):
    def __str__(self) -> str:
        return "int"


class Float(DataType):
    def __str__(self) -> str:
        return "float"


class String(DataType):
    def __str__(self) -> str:
        return "string"
