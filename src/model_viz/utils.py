from dotenv import load_dotenv

from model_viz.logging import get_logger

logger = get_logger(__name__)

# load the environment variables
load_dotenv(override=True)


def vulture_ignore(obj):
    """Decorator to ignore vulture warnings for a function."""
    return obj
