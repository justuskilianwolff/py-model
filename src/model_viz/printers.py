import ast

from model_viz.logging import get_logger

from .utils import indicate_access_level

logger = get_logger(__name__)


def print_function(function: ast.FunctionDef, parameters: bool = True, return_type: bool = True) -> str:
    """
    Return a string representation of a function.

    Args:
        function (ast.FunctionDef): The function to print.

    Returns:
        str: The string representation of the function.
    """
    # Function name
    function_str = indicate_access_level(function.name)

    # add opening parenthesis
    function_str += "("

    if parameters:
        # iterate over function arguments
        for arg in function.args.args:
            if arg.arg == "self":
                continue
            else:
                if isinstance(arg.annotation, ast.Name):
                    function_str += f"{arg.arg}: {arg.annotation.id}, "  # TODO: fix
                else:
                    raise NotImplementedError()
        # remove trailing comma and space
        if function_str.endswith(", "):
            function_str = function_str[:-2]

    # add closing parenthesis
    function_str += ")"

    if return_type:
        # Function return type
        if isinstance(function.returns, ast.Constant):
            function_str += " -> None"
        elif isinstance(function.returns, ast.Name):
            function_str += f" -> {function.returns.id}"
        else:
            # TODO: Implement support for more return types (e.g. List, Dict, Tuple, etc.)
            logger.warning(f"Unknown return type for function: {function.name}")

    return function_str

