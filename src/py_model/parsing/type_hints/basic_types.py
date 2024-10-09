from __future__ import annotations

from typing import Any

from py_model.parsing import BuildingBlock


class TypeHint(BuildingBlock):
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TypeHint):
            return NotImplemented
        return self.__class__ is other.__class__

    def __repr__(self) -> str:
        # for debugging
        return self.__str__()

    def typescript(self) -> str:
        return self.__str__()

    def dot(self) -> str:
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

    def typescript(self) -> str:
        raise ValueError("Type hints must be specified for converting to Typescript")


class NoneType(TypeHint):
    def __str__(self) -> str:
        return "None"

    def typescript(self) -> str:
        return "null"


class Boolean(TypeHint):
    def __str__(self) -> str:
        return "bool"

    def typescript(self) -> str:
        return "boolean"


class Integer(TypeHint):
    def __str__(self) -> str:
        return "int"

    def typescript(self) -> str:
        return "number"


class Float(TypeHint):
    def __str__(self) -> str:
        return "float"

    def typescript(self) -> str:
        return "number"


class String(TypeHint):
    def __str__(self) -> str:
        return "string"
