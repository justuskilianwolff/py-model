from model_viz.logging import get_logger

logger = get_logger(__name__)


def vulture_ignore(obj):
    """Decorator to ignore vulture warnings for a function."""
    return obj


def indicate_access_level(name: str) -> str:
    """Indicate access level of a class, function or attribute."""

    if name.startswith("__"):
        # double underscore indicates private
        return "- " + name[2:]
    elif name.startswith("_"):
        # single underscore indicates protected
        return "# " + name[1:]
    else:
        # no underscore indicates public
        return "+ " + name
