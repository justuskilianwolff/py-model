from __future__ import annotations

import ast
from dataclasses import dataclass


class DataType:
    @classmethod
    def handle_ast(cls, obj: ast.Name):
        if isinstance(obj, ast.Name):
            MATCHING = {
                "None": NoneType(),
                "int": Integer(),
                "float": Float(),
                "str": String(),
                "tuple": Tuple(),
                "Enum": Enumeration(),
            }
            return MATCHING[obj.id]
        else:
            print('please implement')


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
    def handle_slice(self, slice: ast.Tuple):
        for obj in slice.dims:
            if isinstance(obj, ast.Name):
                pass

                print("jhi")
                pass
            else:
                pass


@dataclass
class Tuple(DataType, Sequence):
    def __init__(self, slice: ast.Tuple | None = None):
        self.inner_dtypes: list[DataType] | None = None

    def __str__(self) -> str:
        if self.inner_dtypes is None:
            return "tuple"
        else:
            return f'tuple[{",".join([str(dtype) for dtype in self.inner_dtypes])}]'


class Enumeration(DataType):
    def __str__(self) -> str:
        return "Enum"
