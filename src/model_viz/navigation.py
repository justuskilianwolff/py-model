import ast
import os
from ast import ClassDef

from model_viz.logging import get_logger

logger = get_logger(__name__)


def get_filepath_set(dirs: list[str] | None = None, files: list[str] | None = None) -> set[str]:
    """Get the set of file paths to search for model classes."""
    if (dirs is None) and (files is None):
        raise ValueError("No directories or files provided.")

    # declare set to store file paths
    filepaths = set()

    # add files
    if files is not None:
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")
            if file.endswith(".py"):
                filepaths.add(file)
            else:
                logger.warning(f"File is not a python file: {file}")

    # add directories
    if dirs is not None:
        for directory in dirs:
            for root, _, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith(".py"):
                        filepaths.add(os.path.join(root, filename))

    # check if any files were found
    if len(filepaths) == 0:
        raise ValueError("No files found in provided dirs and files.")

    return filepaths


def get_classes(filepath: str) -> list[ClassDef]:
    with open(filepath, "r") as file:
        tree = ast.parse(file.read(), filename=filepath)

    # get all class definitions
    nodes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    return nodes
