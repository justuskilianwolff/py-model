import ast

from model_viz.datatypes import DataType, Enumeration, Float, Integer, List, NoneType, String, Tuple, Undefined
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
        return MATCHING[annotation.id]
    elif isinstance(annotation, ast.Subscript):
        slice = annotation.slice
        # combined Datatype, e.g.: function -> tuple[int, float]:
        if isinstance(slice, ast.Name):
            try:
                logger.info(f"Key error: {slice.id}")
                return Tuple(inner_dtypes=[MATCHING[slice.id]])
            except KeyError:
                # the inner type is not a basic type and might be a class
                # TODO: what happens if this is not a class
                return Tuple(inner_dtypes=[slice.id])
        elif isinstance(slice, (ast.Tuple, ast.List)):
            inner_dtypes = [handle_type_annotation(inner_type) for inner_type in annotation.slice.elts]
            if isinstance(slice, ast.Tuple):
                return Tuple(inner_dtypes=inner_dtypes)
            elif isinstance(slice, ast.List):
                return List(inner_dtypes=inner_dtypes)
            else:
                raise ValueError("Should not reach here")
        else:
            raise NotImplementedError("Subscript type not implemented")
    else:
        raise NotImplementedError("Type annotation not implemented")
