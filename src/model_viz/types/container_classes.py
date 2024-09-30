from __future__ import annotations

import ast

from model_viz.datatypes import DataType, NoneType, Tuple, Undefined
from model_viz.errors import NotImplementedError
from model_viz.logging import get_logger
from model_viz.utils import indicate_access_level
from model_viz.visitors import OuterAssignVisitor

from . import Attribute, Attributes, Parameter

logger = get_logger(__name__)


class Instance:
    """Parent of Function and Class"""

    def __init__(self, body: list[ast.stmt]):
        # set those when walking the body
        self.functions: list[Function] = []
        self.classes: list[Class] = []

        self.walk_body(body=body)

    def walk_body(self, body):
        for body_item in body:
            if isinstance(body_item, ast.FunctionDef):
                self.functions.append(Function(fun=body_item))
            elif isinstance(body_item, ast.ClassDef):
                self.classes.append(Class(cls=body_item))
            elif isinstance(body_item, (ast.AnnAssign, ast.Assign, ast.Expr)):
                continue
            else:
                logger.warning("Not implemented")


class Function(Instance):
    def __init__(self, fun: ast.FunctionDef) -> None:
        self.name = fun.name
        logger.debug(f"Starting with function {self.name}")
        self.parameters: list[Parameter] = self.get_parameters(fun.args.args)
        self.return_type: DataType = self.get_return_type(fun.returns)

        super().__init__(body=fun.body)
        logger.info(f"finished function {self.name}")

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
            return DataType.handle_ast(obj=return_object)
        elif isinstance(return_object, ast.Subscript):
            # e.g. tuple[int, float]
            if isinstance(return_object.slice, ast.Tuple):
                return Tuple(slice=return_object.slice)
            else:
                logger.warning("Not implemented")
        else:
            logger.warning("Not implemented")

            # raise NotImplementedError

    def get_parameters(self, args):
        parameters = []
        for arg in args:
            if arg.arg == "self":
                # skip 'self' argument (the self from the class)
                continue
            else:
                if isinstance(arg.annotation, ast.Name):
                    dtype = DataType.handle_ast(obj=arg.annotation.id)
                elif arg.annotation is None:
                    dtype = Undefined()
                else:
                    raise NotImplementedError()

            parameter = Parameter(name=arg.arg, type=dtype)
            parameters.append(parameter)

        return parameters


class Class(Instance):
    """Represents a class in the data model."""

    def __init__(self, cls: ast.ClassDef, filepath: str | None = None):
        self.class_name: str = cls.name
        self.body = cls.body
        self.is_dataclass: bool = self.determine_is_dataclass(cls)
        self.inherits_from: list[str] = self.get_inheritance(cls)
        self.attributes: Attributes = self.get_attributes(cls)

        super().__init__(body=self.body)

    def __str__(self) -> str:
        name = self.class_name
        inheritance = "inheritance: " + ", ".join([inh for inh in self.inherits_from])
        functions = "functions: " + ", ".join([str(func) for func in self.functions])
        attributes = "attributes: " + str(self.attributes)
        return f"{name}: {inheritance}; {functions}; {attributes}"

    def determine_is_dataclass(self, cls: ast.ClassDef) -> bool:
        is_dataclass = False
        for dec in cls.decorator_list:
            if isinstance(dec, ast.Name):
                if dec.id == "dataclass":
                    is_dataclass = True
                    break
        return is_dataclass

    def get_inheritance(self, cls: ast.ClassDef) -> list[str]:
        inherits_from = []
        for base in cls.bases:
            if isinstance(base, ast.Name):
                inherits_from.append(base.id)
        # TODO: how are we going to handle import issues like renaming: import x as y?
        return inherits_from

    def get_attributes(self, cls: ast.ClassDef) -> Attributes:
        """Find attributes in constructor in a class.

        Args:
            cls (ast.ClassDef): _description_

        Returns:
            list[Attribute]: _description_
        """

        # store attributes
        attributes = Attributes(attributes=[])

        if self.is_dataclass:
            # is dataclass - take variables in constructor
            for body_item in cls.body:
                # TODO: check that dataclass can only have annotated assignments
                if isinstance(body_item, ast.AnnAssign):
                    attribute = Attribute.handle_annotated_assignment(body_item, is_dataclass=self.is_dataclass)
                    attributes.add_attribute(attribute=attribute)
                else:
                    # no more variable definitions in data class 'style' hence we can break
                    return attributes
        else:
            # not a dataclass, find __init__ method
            init_method = None
            for body_item in cls.body:
                if isinstance(body_item, ast.FunctionDef):
                    if body_item.name == "__init__":
                        init_method = body_item
                        # dont walk init function when walking the body
                        self.body.remove(body_item)
                        break

            if init_method is None:
                logger.error(f"Class {cls.name} does not have an __init__ method.")
                return attributes

            general_assign_visitor = OuterAssignVisitor(class_name=cls.name)
            general_assign_visitor.visit(init_method)

            for node in general_assign_visitor.ann_assigns:
                attribute = Attribute.handle_annotated_assignment(node, is_dataclass=False)
                attributes.add_attribute(attribute=attribute)

            # handle assigns
            for node in general_assign_visitor.assigns:
                attributes.add_attributes(attributes=Attribute.handle_assign(node))

        return attributes
