from __future__ import annotations

import ast

from model_viz.datatypes import MATCHING, DataType, NoneType, Undefined
from model_viz.errors import NotImplementedError
from model_viz.logging import get_logger
from model_viz.utils import indicate_access_level

from .instance import Instance
from .parameter import Parameter

logger = get_logger(__name__)


class Function(Instance):
    def __init__(self, fun: ast.FunctionDef) -> None:
        self.name = fun.name
        self.parameters: list[Parameter] = self.get_parameters(fun.args.args)
        self.return_type: DataType = self.get_return_type(fun.returns)

        super().__init__(definition=fun)

    def __str__(self) -> str:
        str_representation = f"{self.name}({', '.join([str(param) for param in self.parameters])})"
        if self.return_type is not None:
            str_representation += f" -> {self.return_type}"
        return indicate_access_level(str_representation)

    def get_return_type(self, return_object):
        # function return type
        if return_object is None:
            # no return type specified
            return Undefined()
        elif isinstance(return_object, ast.Constant):
            # -> None:
            return NoneType()
        elif isinstance(return_object, ast.Name):
            # -> int:, str:, etc.
            return MATCHING[str(return_object.id)]
        else:
            raise NotImplementedError

    def get_parameters(self, args):
        parameters = []
        for arg in args:
            if arg.arg == "self":
                # skip 'self' argument (the self from the class)
                continue
            else:
                if isinstance(arg.annotation, ast.Name):
                    dtype = MATCHING[str(arg.id)]
                elif arg.annotation is None:
                    dtype = Undefined()
                else:
                    raise NotImplementedError()

            parameter = Parameter(name=arg.arg, type=dtype)
            parameters.append(parameter)

        return parameters
