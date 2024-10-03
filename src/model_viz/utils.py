import ast

from model_viz.datatypes import (
    CustomClass,
    DataType,
    Enumeration,
    Float,
    Integer,
    List,
    NoneType,
    String,
    Tuple,
    Undefined,
    Union,
)
from model_viz.logging import get_logger

logger = get_logger(__name__)


def vulture_ignore(obj):
    """Decorator to ignore vulture warnings for a function."""
    return obj


def indicate_access_level(name: str) -> str:
    """Indicate access level of a class, function or attribute."""

    if name.startswith("__"):
        # double underscore indicates private
        return "-" + name[2:]
    elif name.startswith("_"):
        # single underscore indicates protected
        return "#" + name[1:]
    else:
        # no underscore indicates public
        return "+" + name


def determine_is_dataclass(class_def: ast.ClassDef) -> bool:
    is_dataclass = False
    for dec in class_def.decorator_list:
        if isinstance(dec, ast.Name):
            if dec.id == "dataclass":
                is_dataclass = True
                break
    return is_dataclass


MATCHING = {
    "None": NoneType(),
    "int": Integer(),
    "float": Float(),
    "str": String(),
    "tuple": Tuple(),
    "Enum": Enumeration(),
}


def handle_type_annotation(annotation) -> DataType:
    if annotation is None:
        # no return type specified: function():
        return Undefined()
    elif isinstance(annotation, ast.Constant):
        # None was specified: function() -> None:
        return NoneType()
    elif isinstance(annotation, ast.Name):
        # Datatype was specified, e.g.: function() -> str:
        try:
            return MATCHING[annotation.id]
        except KeyError:
            # if not in matching, it is a custom class
            return CustomClass(name=annotation.id)
    elif isinstance(annotation, ast.Subscript):
        # obtain value
        value = annotation.value
        if isinstance(annotation.slice, ast.Name):
            inner_dtypes = [handle_type_annotation(annotation.slice)]
        else:
            inner_dtypes = [handle_type_annotation(inner_type) for inner_type in annotation.slice.elts]

        if value.id == "list":
            # list Datatype, e.g.: function -> list[str]:
            return List(inner_dtypes=inner_dtypes)
        elif value.id == "tuple":
            # tuple Datatype, e.g.: function -> tuple[str, int]:
            return Tuple(inner_dtypes=inner_dtypes)
        else:
            raise NotImplementedError("Subscript type not implemented")
    elif isinstance(annotation, ast.BinOp):
        if isinstance(annotation.op, ast.BitOr):
            # make sure pipe is used for Union, e.g.: function() -> str | int:
            inner_dtypes = []
            # obtain left and right dtypes
            left = handle_type_annotation(annotation.left)
            right = handle_type_annotation(annotation.right)
            if isinstance(left, Union):
                inner_dtypes.extend(left.inner_dtypes)
            if isinstance(right, Union):
                inner_dtypes.extend(right.inner_dtypes)
            return Union(inner_dtypes=[left, right])
        else:
            raise NotImplementedError("Binary operation not implemented")
    else:
        raise NotImplementedError("Type annotation not implemented")
