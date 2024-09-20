import ast

from model_viz.logging import get_logger

from .errors import NotImplementedError

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


def handle_function_arg(arg: ast.arg) -> tuple[str, str | None]:
    """Handle function argument."""

    if isinstance(arg.annotation, ast.Name):
        tp = arg.annotation.id
    elif arg.annotation is None:
        tp = None
    else:
        raise NotImplementedError()
    
    return arg.arg, tp
