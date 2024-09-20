import ast

from model_viz.logging import get_logger

from .errors import NotImplementedError
from .utils import handle_function_arg, indicate_access_level

logger = get_logger(__name__)


def get_func_repr(function: ast.FunctionDef, parameters: bool = True, return_type: bool = True) -> str:
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
                # skip 'self' argument
                continue
            else:
                name, tp = handle_function_arg(arg)
                function_str += f"{name}: {tp}, " if tp else f"{name}, "

        # remove trailing comma and space if there are any
        if function_str.endswith(", "):
            function_str = function_str[:-2]

    # add closing parenthesis
    function_str += ")"

    if return_type:
        # Function return type
        if function.returns is None:
            # no return type specified
            pass
        elif isinstance(function.returns, ast.Constant):
            # -> None:
            function_str += " -> None"
        elif isinstance(function.returns, ast.Name):
            # -> int:, str:, etc.
            function_str += f" -> {function.returns.id}"
        else:
            # TODO: Implement support for more return types (e.g. List, Dict, Tuple, etc.)
            function_str += " -> complex dtype (not implemented yet)"
            logger.warning(f"Unknown return type for function: {function.name}")

    return function_str


def get_attr_repr(attribute: ast.AnnAssign | ast.Assign, type: bool = True) -> str:
    """
    Return a string representation of an attribute.

    Args:
        attribute (ast.AnnAssign | ast.Assign): The attribute to print.

    Returns:
        str: The string representation of the attribute.
    """
    if isinstance(attribute, ast.Assign):
        attribute_str = indicate_access_level(attribute.value.id)
    elif isinstance(attribute, ast.AnnAssign):
        attribute_str = indicate_access_level(attribute.target.id)
        if type:
            if isinstance(attribute.annotation, ast.Name):
                attribute_str += f": {attribute.annotation.id}"
            else:
                attribute_str += ": not implemented"
                logger.warning(f"Unknown attribute type for attribute: {attribute.target.id}")
    else:
        raise NotImplementedError()

    return attribute_str
