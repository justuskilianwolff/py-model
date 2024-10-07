from __future__ import annotations

from typing import Any


class TypeHint:
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TypeHint):
            return NotImplemented
        return self.__class__ is other.__class__

    def __repr__(self) -> str:
        # for debugging
        return self.__str__()


class CustomClass(TypeHint):
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Any):
        if not isinstance(other, CustomClass):
            return NotImplemented
        return self.name == other.name


class Undefined(TypeHint):
    def __str__(self) -> str:
        return ""


class NoneType(TypeHint):
    def __str__(self) -> str:
        return "None"


class Boolean(TypeHint):
    def __str__(self) -> str:
        return "bool"


class Integer(TypeHint):
    def __str__(self) -> str:
        return "int"


class Float(TypeHint):
    def __str__(self) -> str:
        return "float"


class String(TypeHint):
    def __str__(self) -> str:
        return "string"
