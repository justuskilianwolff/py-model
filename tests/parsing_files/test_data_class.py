import os
from dataclasses import dataclass

from py_model.datatypes import String, Undefined
from py_model.navigation import get_classes
from py_model.types import Attribute, Attributes, Class, Function


@dataclass
class Person:
    name: str

    def greet(self):
        return f"Hello {self.name}"


def test_simple_class():
    # what we expect to get
    class_expected: Class = Class(
        name="Person",
        attributes=Attributes(attributes=[Attribute(name="name", dtype=String())]),
        is_dataclass=True,
        inherits_from=[],
        functions=[Function(name="greet", parameters=[], return_type=Undefined())],
        classes=[],
    )

    # get the file path
    filepath = os.path.abspath(__file__)
    class_def = get_classes(filepath)[0]
    class_created = Class.from_ast(class_def=class_def)

    assert class_created == class_expected
