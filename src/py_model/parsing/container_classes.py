from __future__ import annotations

import ast

from py_model.logging import get_logger
from py_model.parsing import BuildingBlock
from py_model.utils import determine_is_dataclass, handle_type_annotation, indicate_access_level
from py_model.visitors import OuterAssignVisitor
from py_model.writing import SupportedTypes

from . import Attribute, Attributes, Parameter
from .type_hints.basic_types import NoneType, TypeHint, Undefined

logger = get_logger(__name__)


class Instance(BuildingBlock):
    """Parent of Function and Class"""

    def __init__(self, functions: list[Function] = [], classes: list[Class] = []) -> None:
        # set those when walking the body
        self.functions: list[Function] = functions
        self.classes: list[Class] = classes

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return vars(self) == vars(other)

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def get_functions_and_classes(cls, body, needs_annotation: bool) -> tuple[list[Function], list[Class]]:
        functions = []
        classes = []
        for body_item in body:
            if isinstance(body_item, ast.FunctionDef):
                functions.append(Function.from_ast(body_item, needs_annotation=needs_annotation))
            elif isinstance(body_item, ast.ClassDef):
                classes.append(Class.from_ast(body_item, needs_annotation=needs_annotation))

        return functions, classes


class Function(Instance):
    def __init__(
        self,
        name: str,
        parameters: list[Parameter],
        return_type: TypeHint,
        functions: list[Function] = [],
        classes: list[Class] = [],
    ) -> None:
        self.name = name
        self.parameters: list[Parameter] = parameters
        self.return_type: TypeHint = return_type
        self.functions: list[Function] = functions
        self.classes: list[Class] = classes

    @classmethod
    def from_ast(cls, fun: ast.FunctionDef, needs_annotation: bool):
        name = fun.name
        parameters = cls.get_parameters(fun.args.args, needs_annotation=needs_annotation)
        return_type = cls.get_return_type(fun.returns)

        # generate lists of functions and classes
        functions, classes = cls.get_functions_and_classes(fun.body, needs_annotation=needs_annotation)

        return cls(name=name, parameters=parameters, return_type=return_type, functions=functions, classes=classes)

    @classmethod
    def get_return_type(cls, return_object) -> TypeHint:
        return handle_type_annotation(return_object)

    @classmethod
    def get_parameters(cls, args, needs_annotation: bool):
        parameters = []
        for arg in args:
            if arg.arg == "self":
                # skip 'self' argument, e.g.: function(self, arg1):
                # DISCUSS: handle class functions in here?
                continue
            else:
                dtype = handle_type_annotation(arg.annotation, needs_annotation=needs_annotation)

            parameter = Parameter(name=arg.arg, dtype=dtype)
            parameters.append(parameter)

        return parameters

    def __str__(self) -> str:
        str_representation = f"{self.name}({', '.join([str(param) for param in self.parameters])})"

        # if return type is not Undefined, add it to the string representation
        if not isinstance(self.return_type, Undefined):
            str_representation += f" -> {self.return_type}"
        return indicate_access_level(str_representation)

    def typescript(self) -> str:
        params = ", ".join([param.get_string(supported_type=SupportedTypes.ts) for param in self.parameters])

        if isinstance(self.return_type, (Undefined, NoneType)):
            ret = "void"
        else:
            ret = self.return_type.get_string(supported_type=SupportedTypes.ts)

        return f"{self.name}({params}): {ret};"

    def dot(self) -> str:
        return self.__str__()


class Class(Instance):
    """Represents a class in the data model."""

    def __init__(
        self,
        name: str,
        is_dataclass: bool,
        inherits_from: list[str],
        attributes: Attributes,
        functions: list[Function] = [],
        classes: list[Class] = [],
    ) -> None:
        self.name = name
        self.is_dataclass: bool = is_dataclass
        self.inherits_from: list[str] = inherits_from
        self.attributes: Attributes = attributes
        self.functions: list[Function] = functions
        self.classes: list[Class] = classes

    @classmethod
    def from_ast(cls, class_def: ast.ClassDef, needs_annotation: bool) -> Class:
        name = class_def.name
        is_dataclass = determine_is_dataclass(class_def=class_def)
        inherits_from = cls.get_inheritance(class_def=class_def)
        attributes, body = cls.get_attributes(
            class_def=class_def, is_dataclass=is_dataclass, needs_annotation=needs_annotation
        )
        functions, classes = Instance.get_functions_and_classes(body, needs_annotation=needs_annotation)

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
    def get_attributes(
        cls, class_def: ast.ClassDef, is_dataclass: bool, needs_annotation: bool
    ) -> tuple[Attributes, list]:
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
                    attribute = Attribute.handle_annotated_assignment(body_item)
                    attributes.add_attribute(new_attr=attribute)
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
                attribute = Attribute.handle_annotated_assignment(node)
                attributes.add_attribute(new_attr=attribute)

            # handle assigns
            for node in general_assign_visitor.assigns:
                if needs_annotation:
                    raise ValueError("Annotation needed to obtain desired file format.")
                else:
                    attributes.add_attributes(
                        attributes=Attribute.handle_assign(
                            node,
                        )
                    )
        return attributes, body

    def __str__(self) -> str:
        name = self.name
        inheritance = "inheritance: " + ", ".join([inh for inh in self.inherits_from])
        attributes = "attributes: " + str(self.attributes)
        functions = "functions: " + ", ".join([str(func) for func in self.functions])
        return f"{name}: \n {inheritance}; \n {attributes}; \n {functions}"

    def typescript(self) -> str:
        string_repr = f"interface {self.name} "

        if len(self.inherits_from) >= 1:
            string_repr += "extends "
            for inheritance in self.inherits_from:
                string_repr += f"{inheritance}, "

            # remove last character (the comma)
            string_repr = string_repr[:-2]

        string_repr += "{ \n"

        for attribute in self.attributes.attributes:
            string_repr += f"{attribute.get_string(supported_type=SupportedTypes.ts)}; \n"

        for func in self.functions:
            string_repr += f"{func.get_string(supported_type=SupportedTypes.ts)} \n"

        string_repr += "}\n"

        return string_repr

    def dot(self) -> str:
        return self.__str__()
