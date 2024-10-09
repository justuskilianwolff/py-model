import ast
import os

from py_model.errors import MissingImplementationError
from py_model.logging import get_logger
from py_model.parsing.type_hints import (
    Boolean,
    CustomClass,
    Dict,
    Float,
    Integer,
    List,
    NoneType,
    Set,
    String,
    Tuple,
    TypeHint,
    Undefined,
    Union,
)

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
    """Determine if a class is a dataclass."""
    is_dataclass = False
    for dec in class_def.decorator_list:
        if isinstance(dec, ast.Name):
            if dec.id == "dataclass":
                is_dataclass = True
                break
    return is_dataclass


def handle_type_annotation(annotation) -> TypeHint:
    if annotation is None:
        # no return type specified: function():
        return Undefined()
    elif isinstance(annotation, ast.Constant):
        # None was specified: function() -> None:
        return NoneType()
    elif isinstance(annotation, ast.Name):
        # Datatype was specified, e.g.: function() -> str:
        MATCHING = {
            "None": NoneType(),
            "bool": Boolean(),
            "int": Integer(),
            "float": Float(),
            "str": String(),
        }
        try:
            return MATCHING[annotation.id]
        except KeyError:
            # if not in matching, it is a custom class
            return CustomClass(name=annotation.id)
    elif isinstance(annotation, ast.Subscript):
        # nested datatype like list or tuple, e.g.: function() -> list[str]:
        value = annotation.value  # obtain value (tuple or list)
        if isinstance(annotation.slice, ast.Name):
            # single instace of datatype, e.g.: function -> list[str]:
            dtypes = [handle_type_annotation(annotation.slice)]
        elif isinstance(annotation.slice, ast.Tuple):
            # multiple instances of datatype, e.g.: function -> list[str, int]:
            dtypes = [handle_type_annotation(inner_type) for inner_type in annotation.slice.elts]
        elif isinstance(annotation.slice, ast.Subscript):
            # nested list or tuple, e.g.: function -> list[list[str]]:
            dtypes = [handle_type_annotation(annotation.slice)]
        else:
            raise MissingImplementationError("Subscript slice not implemented")

        if isinstance(value, ast.Name):
            if value.id == "list":
                # list Datatype, e.g.: function -> list[str]:
                return List(dtypes=dtypes)
            elif value.id == "tuple":
                # tuple Datatype, e.g.: function -> tuple[str, int]:
                return Tuple(dtypes=dtypes)
            elif value.id == "dict":
                return Dict(dtypes=dtypes)
            elif value.id == "set":
                return Set(dtypes=dtypes)
            else:
                raise MissingImplementationError(f"Neither list nor tuple, not implemented for {value.id}.")
        else:
            raise MissingImplementationError("Subscript type not implemented")

    elif isinstance(annotation, ast.BinOp):
        if isinstance(annotation.op, ast.BitOr):
            # make sure pipe is used for Union, e.g.: function() -> str | int:
            dtypes = []
            # obtain left and right dtypes
            left = handle_type_annotation(annotation.left)
            right = handle_type_annotation(annotation.right)
            if isinstance(left, Union):
                dtypes.extend(left.dtypes)
            if isinstance(right, Union):
                dtypes.extend(right.dtypes)

            return Union(dtypes=[left, right])

        else:
            raise MissingImplementationError("Binary operation not implemented")
    else:
        raise MissingImplementationError("Type annotation not implemented")


def set_project_name(name: str) -> None:
    """
    Set the project name for the files and in the file content to not manually change from the template.
    """

    mapping = {"py-model": name, "py_model": name.replace("-", "_")}

    dirs_to_remove = set()

    for root, _, files in os.walk("."):
        # skip all hidden directories
        if "/." in root:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r", errors="ignore") as f:
                content = f.read()

            for old, new in mapping.items():
                content = content.replace(old, new)

            with open(file_path, "w") as f:
                f.write(content)

            # check if file needs moving
            if any(key in file_path for key in mapping.keys()):
                # move the file to the new name
                new_file_path = file_path
                for old, new in mapping.items():
                    new_file_path = new_file_path.replace(old, new)

                # create dirs if not exist
                dirs_new = os.path.dirname(new_file_path)
                os.makedirs(dirs_new, exist_ok=True)

                # move file
                os.rename(file_path, new_file_path)

                # delete old dirs
                dirs_old = os.path.dirname(file_path)
                dirs_to_remove.add(dirs_old)

    # remove old dirs
    for dir_to_remove in dirs_to_remove:
        os.removedirs(dir_to_remove)
