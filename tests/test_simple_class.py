import os

from model_viz.datatypes import String, Undefined
from model_viz.navigation import get_classes
from model_viz.types import Attribute, Attributes, Class, Function


class Person:
    def __init__(self, name: str):
        self.name: str = name

    def greet(self):
        return f"Hello {self.name}"


def test_simple_class():
    # what we expect to get
    class_expected: Class = Class(
        name="Person",
        attributes=Attributes(attributes=[Attribute(name="name", dtype=String())]),
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
