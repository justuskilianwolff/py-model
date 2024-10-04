import os

from py_model.datatypes import String, Undefined
from py_model.navigation import get_classes
from py_model.types import Attribute, Attributes, Class, Function


class Person:
    def __init__(self, name: str, age: int):
        self.name: str = name
        self.age = age

    def greet(self):
        return f"Hello {self.name}"


def test_simple_class():
    # what we expect to get
    class_expected: Class = Class(
        name="Person",
        attributes=Attributes(
            attributes=[Attribute(name="name", dtype=String()), Attribute(name="age", dtype=Undefined())]
        ),
        is_dataclass=False,
        inherits_from=[],
        functions=[Function(name="greet", parameters=[], return_type=Undefined())],
        classes=[],
    )

    # get the file path
    filepath = os.path.abspath(__file__)
    class_def = get_classes(filepath)[0]
    class_created = Class.from_ast(class_def=class_def)

    assert class_created == class_expected


def test_adding_attribute():
    attribute = Attribute(name="name", dtype=Undefined())

    attributes = Attributes(attributes=[attribute])

    attribute_with_th = Attribute(name="name", dtype=String())

    attributes.add_attribute(new_attr=attribute_with_th)

    # we excpet only one attribute
    assert len(attributes.attributes) == 1
    assert attributes.attributes[0] == attribute_with_th

    # lets do it the other way around
    attributes = Attributes(attributes=[attribute_with_th])
    attributes.add_attribute(new_attr=attribute)

    # we excpet only one attribute
    assert len(attributes.attributes) == 1
    assert attributes.attributes[0] == attribute_with_th
