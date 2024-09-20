from __future__ import annotations

import ast

from model_viz.logging import get_logger
from model_viz.utils import indicate_access_level

from .parameter import Parameter

logger = get_logger(__name__)


class Function:
    def __init__(self, name: str, parameters: list[Parameter], return_type: str | None) -> None:
        self.name = name
        self.parameters = parameters
        self.return_type = return_type

    def __str__(self) -> str:
        str_representation = f"{self.name}({', '.join([str(param) for param in self.parameters])})"
        if self.return_type is not None:
            str_representation += f" -> {self.return_type}"
        return indicate_access_level(str_representation)

    @classmethod
    def create_function(cls, func: ast.FunctionDef) -> Function:
        # function return type
        if func.returns is None:
            # no return type specified
            return_type = None
        elif isinstance(func.returns, ast.Constant):
            # -> None:
            return_type = "None"
        elif isinstance(func.returns, ast.Name):
            # -> int:, str:, etc.
            return_type = func.returns.id
        else:
            # TODO: Implement support for more return types (e.g. List, Dict, Tuple, etc.)
            return_type = "complex dtype (not implemented yet)"
            logger.warning(f"Unknown return type for function: {func.name}")
        
        # TODO: handle inner functions and classes (v2)
        parameters = []
        for arg in func.args.args:
            if arg.arg == "self":
                # skip 'self' argument
                continue
            else:
                if isinstance(arg.annotation, ast.Name):
                    tp = arg.annotation.id
                elif arg.annotation is None:
                    tp = None
                else:
                    raise NotImplementedError()

            parameter = Parameter(name=arg.arg, type=tp)
            parameters.append(parameter)

        return cls(name=func.name, parameters=parameters, return_type=return_type)
