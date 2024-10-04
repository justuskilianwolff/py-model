from __future__ import annotations

import ast

from py_model.datatypes import Undefined
from py_model.errors import MissingImplementationError
from py_model.utils import handle_type_annotation, indicate_access_level

from .typehintablevalue import TypeHintableValue


class Attribute(TypeHintableValue):
    def __str__(self) -> str:
        return indicate_access_level(super().__str__())

    def has_type(self) -> bool:
        return self.dtype is not None

    @classmethod
    def handle_annotated_assignment(cls, node: ast.AnnAssign) -> Attribute:
        # obtain name
        if isinstance(node.target, ast.Attribute):
            # happens when
            name = node.target.attr
        elif isinstance(node.target, ast.Name):
            name = node.target.id
        else:
            raise MissingImplementationError()

        # get annotation
        dtype = handle_type_annotation(node.annotation)
        return Attribute(name=name, dtype=dtype)

    @classmethod
    def handle_assign(cls, node: ast.Assign) -> list[Attribute]:
        attributes = []
        for target in node.targets:
            # check that this actually is a self. attribute
            if isinstance(target, ast.Attribute):
                if isinstance(target.value, ast.Name):
                    if target.value.id != "self":
                        continue
                else:
                    raise MissingImplementationError()

                name = target.attr

                # add attribute to list
                attributes.append(Attribute(name=name, dtype=Undefined()))

        return attributes
