import ast

from model_viz.logging import get_logger

from ..visitors import OuterAssignVisitor
from . import Attribute, Attributes, Instance

logger = get_logger(__name__)


class Class(Instance):
    """Represents a class in the data model."""

    def __init__(self, cls: ast.ClassDef, filepath: str | None = None):
        self.class_name: str = cls.name
        self.body = cls.body
        self.is_dataclass: bool = self.determine_is_dataclass(cls)
        self.inherits_from: list[str] = self.get_inheritance(cls)
        self.attributes: Attributes = self.get_attributes(cls)

        super().__init__(definition=cls)

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
                        self.body.remove(body_item)  # TODO: check this actually works
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
