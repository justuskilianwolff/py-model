from __future__ import annotations

import ast

from model_viz.datatypes import DataType, NoneType, Tuple, Undefined
from model_viz.errors import NotImplementedError
from model_viz.logging import get_logger
from model_viz.utils import determine_is_dataclass, indicate_access_level
from model_viz.visitors import OuterAssignVisitor

from . import Attribute, Attributes, Parameter

logger = get_logger(__name__)


class Instance:
    """Parent of Function and Class"""

    def __init__(self, functions: list[Function] = [], classes: list[Class] = []) -> None:
        # set those when walking the body
        self.functions: list[Function] = functions
        self.classes: list[Class] = classes

    @classmethod
    def get_functions_and_classes(cls, body) -> tuple[list[Function], list[Class]]:
        functions = []
        classes = []
        for body_item in body:
            if isinstance(body_item, ast.FunctionDef):
                functions.append(Function.from_ast(body_item))
            elif isinstance(body_item, ast.ClassDef):
                classes.append(Class.from_ast(body_item))
            elif isinstance(body_item, (ast.AnnAssign, ast.Assign, ast.Expr)):
                # TODO: what cases are these?? Document
                continue
            else:
                logger.warning(f"Not implemented for {type(body_item)}")

        return functions, classes


class Function(Instance):
    def __init__(
        self,
        name: str,
        parameters: list[Parameter],
        return_type: DataType,
        functions: list[Function] = [],
        classes: list[Class] = [],
    ) -> None:
        self.name = name
        self.parameters: list[Parameter] = parameters
        self.return_type: DataType = return_type
        self.functions: list[Function] = functions
        self.classes: list[Class] = classes

    @classmethod
    def from_ast(cls, fun: ast.FunctionDef):
        name = fun.name
        parameters = cls.get_parameters(fun.args.args)
        return_type = cls.get_return_type(fun.returns)

        # generate lists of functions and classes
        functions, classes = Instance.get_functions_and_classes(fun.body)

        return cls(name=name, parameters=parameters, return_type=return_type, functions=functions, classes=classes)

    @classmethod
    def get_return_type(cls, return_object) -> DataType:
        # get the return type of a function
        if return_object is None:
            # no return type specified: function():
            return Undefined()
        elif isinstance(return_object, ast.Constant):
            # None was specified: function() -> None:
            return NoneType()
        elif isinstance(return_object, ast.Name):
            # Datatype was specified, e.g.: function() -> str:
            return DataType.handle_ast(obj=return_object)
        elif isinstance(return_object, ast.Subscript):
            # combined Datatype, e.g.: function -> tuple[int, float]:
            if isinstance(return_object.slice, ast.Tuple):
                return Tuple(slice=return_object.slice)
            else:
                logger.warning("Return type implemented for subscript")
        else:
            # TODO: implement
            logger.warning("Return type not implemented")

        return Undefined()

    @classmethod
    def get_parameters(cls, args):
        parameters = []
        for arg in args:
            if arg.arg == "self":
                # skip 'self' argument, e.g.: function(self, arg1):
                # DISCUSS: handle class functions in here?
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

    def __str__(self) -> str:
        str_representation = f"{self.name}({', '.join([str(param) for param in self.parameters])})"
        if self.return_type is not None:
            str_representation += f" -> {self.return_type}"
        return indicate_access_level(str_representation)


class Class(Instance):
    """Represents a class in the data model."""

    def __init__(
        self,
        name: str,
        is_dataclass: bool,
        inherits_from: list[str],
        attributes: Attributes,
        functions: list[Function],
        classes: list[Class],
    ) -> None:
        self.name = name
        self.is_dataclass: bool = is_dataclass
        self.inherits_from: list[str] = inherits_from
        self.attributes: Attributes = attributes
        self.functions: list[Function] = functions
        self.classes: list[Class] = classes

    @classmethod
    def from_ast(cls, class_def: ast.ClassDef) -> Class:
        name = class_def.name
        is_dataclass = determine_is_dataclass(class_def=class_def)
        inherits_from = cls.get_inheritance(class_def=class_def)
        attributes, body = cls.get_attributes(class_def=class_def, is_dataclass=is_dataclass)
        functions, classes = Instance.get_functions_and_classes(body)

        return Class(
            name=name,
            is_dataclass=is_dataclass,
            inherits_from=inherits_from,
            attributes=attributes,
            functions=functions,
            classes=classes,
        )

    @classmethod
    def get_inheritance(cls, class_def: ast.ClassDef) -> list[str]:
        inherits_from = []
        for base in class_def.bases:
            if isinstance(base, ast.Name):
                inherits_from.append(base.id)
        # TODO: how are we going to handle import issues like renaming: import x as y?
        return inherits_from

    @classmethod
    def get_attributes(cls, class_def: ast.ClassDef, is_dataclass: bool) -> tuple[Attributes, list]:
        """Find attributes in constructor in a class.

        Args:
            cls (ast.ClassDef): _description_

        Returns:
            list[Attribute]: _description_
        """
        # get body
        body = class_def.body  # TODO: what dtype is this?

        # store attributes
        attributes = Attributes(attributes=[])

        if is_dataclass:
            # is dataclass - take variables in constructor
            for body_item in body:
                # TODO: check that dataclass can only have annotated assignments
                if isinstance(body_item, ast.AnnAssign):
                    attribute = Attribute.handle_annotated_assignment(body_item, is_dataclass=is_dataclass)
                    attributes.add_attribute(attribute=attribute)
                else:
                    # no more variable definitions in data class 'style' hence we can break
                    return attributes, body
        else:
            # not a dataclass, find __init__ method
            init_method = None
            for body_item in body:
                if isinstance(body_item, ast.FunctionDef):
                    if body_item.name == "__init__":
                        init_method = body_item
                        # dont walk init function when walking the body
                        body.remove(body_item)
                        break

            if init_method is None:
                logger.error(f"Class {class_def.name} does not have an __init__ method.")
                return attributes, body

            general_assign_visitor = OuterAssignVisitor(class_name=class_def.name)
            general_assign_visitor.visit(init_method)

            for node in general_assign_visitor.ann_assigns:
                attribute = Attribute.handle_annotated_assignment(node, is_dataclass=False)
                attributes.add_attribute(attribute=attribute)

            # handle assigns
            for node in general_assign_visitor.assigns:
                attributes.add_attributes(attributes=Attribute.handle_assign(node))

        return attributes, body

    def __str__(self) -> str:
        name = self.name
        inheritance = "inheritance: " + ", ".join([inh for inh in self.inherits_from])
        functions = "functions: " + ", ".join([str(func) for func in self.functions])
        attributes = "attributes: " + str(self.attributes)
        return f"{name}: \n {inheritance}; \n {functions}; \n {attributes}"
