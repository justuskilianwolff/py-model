from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from py_model.logging import get_logger

from .attribute import Attribute

logger = get_logger(__name__)


@dataclass
class Attributes:
    attributes: list[Attribute]

    def contains_attribute(self, attribute: Attribute) -> Attribute | Literal[False]:
        for attr in self.attributes:
            if attr.name == attribute.name:
                return attr
        return False

    def add_attribute(self, new_attr: Attribute) -> None:
        # check if attribute is already in list
        if old_attr := self.contains_attribute(attribute=new_attr):
            logger.info(f"Attribute {new_attr.name} is already in the list of attributes.")
            # check if the attribute has a type hint
            if new_attr.has_type():
                raise ValueError(f"Attribute {new_attr.name} has different type hints.")
            else:
                logger.info(f"Adding type hint {new_attr.dtype} to attribute '{new_attr.name}'.")
                old_attr.dtype = new_attr.dtype
        else:
            self.attributes.append(new_attr)

    def add_attributes(self, attributes: list[Attribute]) -> None:
        for attribute in attributes:
            self.add_attribute(new_attr=attribute)

    def __str__(self) -> str:
        return ", ".join([str(attr) for attr in self.attributes])

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return vars(self) == vars(other)
