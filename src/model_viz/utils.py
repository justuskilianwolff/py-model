from model_viz.logging import get_logger

logger = get_logger(__name__)


def vulture_ignore(obj):
    """Decorator to ignore vulture warnings for a function."""
    return obj
