from __future__ import annotations

import ast

from py_model.datatypes import Undefined
from py_model.errors import MissingImplementationError
from py_model.utils import handle_type_annotation, indicate_access_level
from py_model.visitors import AttributeVisitor

from .typehintablevalue import TypeHintableValue


class Attribute(TypeHintableValue):
    def __str__(self) -> str:
        return indicate_access_level(super().__str__())

    def has_type(self) -> bool:
        return isinstance(self.dtype, Undefined)

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
        def handle_attribute(attr: ast.Attribute) -> Attribute | None:
            # obtain name
            name = attr.attr

            if isinstance(attr.value, ast.Name):
                if (attr.value.id == "self") and isinstance(attr.ctx, ast.Store):
                    # if it is not a member of store we can ignore it (otherwise we add functions as an attribute)
                    return Attribute(name=name, dtype=Undefined())
                else:
                    return None
            else:
                raise MissingImplementationError()

        attributes = []

        # extract all ast.Attribute nodes
        attribute_visitor = AttributeVisitor()
        attribute_visitor.visit(node)

        for attr in attribute_visitor.attributes:
            attribute = handle_attribute(attr)
            if attribute:
                attributes.append(attribute)

        return attributes
