import os
from dataclasses import dataclass

from py_model.datatypes import Integer, List, String, Tuple
from py_model.navigation import get_classes
from py_model.types import Attribute, Attributes, Class, Function, Parameter


@dataclass
class Person:
    name: list[tuple[tuple[int, str], list[str]]]

    def greet(self, arg: list[tuple[tuple[int, str], list[str]]]) -> str:
        return f"Hello {self.name}"


def test_nested_annotation():
    expected_annotation = List([Tuple([Tuple([Integer(), String()]), List([String()])])])
    # what we expect to get
    expected: Class = Class(
        name="Person",
        attributes=Attributes(attributes=[Attribute(name="name", dtype=expected_annotation)]),
        is_dataclass=True,
        inherits_from=[],
        functions=[
            Function(name="greet", parameters=[Parameter(name="arg", dtype=expected_annotation)], return_type=String())
        ],
        classes=[],
    )

    # get the file path
    filepath = os.path.abspath(__file__)
    class_def = get_classes(filepath)[0]
    created = Class.from_ast(class_def=class_def)

    assert created == expected
