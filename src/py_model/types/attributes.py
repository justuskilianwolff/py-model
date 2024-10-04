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

    def add_attribute(self, attribute: Attribute) -> None:
        # check if attribute is already in list
        if attr := self.contains_attribute(attribute=attribute):
            logger.info(f"Attribute {attribute.name} is already in the list of attributes.")
            # check if the attribute has a type hint
            if attribute.has_type():
                # if it has a type hint, update the type hint of the existing attribute (if that doesnt have one)
                if attr.has_type():
                    logger.info(f"Attribute {attribute.name} already has a type hint: {attr.dtype}.")
                    if attr.dtype != attribute.dtype:
                        logger.warning(f"Attribute {attribute.name} has different type hints.")
                else:
                    logger.info(f"Adding type hint {attribute.dtype} to attribute {attribute.name}.")
                    attr.dtype = attribute.dtype

        self.attributes.append(attribute)

    def add_attributes(self, attributes: list[Attribute]) -> None:
        for attribute in attributes:
            self.add_attribute(attribute=attribute)

    def __str__(self) -> str:
        return ", ".join([str(attr) for attr in self.attributes])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return vars(self) == vars(other)
