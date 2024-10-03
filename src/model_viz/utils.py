import ast

from model_viz.datatypes import DataType, Enumeration, Float, Integer, NoneType, String, Tuple
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


def handle_type_annotation() -> DataType:
    pass
