import os
from dataclasses import dataclass

from py_model.navigation import get_classes
from py_model.parsing import Attribute, Attributes, Class, Function, Parameter
from py_model.parsing.type_hints import Boolean, Dict, Integer, List, Set, String, Tuple, Undefined

filepath = os.path.abspath(__file__)
class_definitions = get_classes(filepath)


@dataclass
class DataClass:
    name: str
    active: bool


@dataclass
class Sequences:
    names: list[str]
    numbers: tuple[int, int]
    pairs: dict[str, str]
    set_int: set[int]


@dataclass
class Nested:
    name: list[dict[tuple[int, str], list[str]]]

    def greet(self, arg: dict[tuple[tuple[int, str], list[str]], list[int]]) -> str:
        return f"Hello {self.name}"


class MissingAnnotation:
    def __init__(self, name) -> None:
        self.name = name

    def return_without_type(self):
        return "A string?"


class ComplexAssignments:
    def __init__(self) -> None:
        (self.first, (self.second, self.third)) = self.return_tuples()

    def return_tuples(self):
        return ("First", ("Second", "Third"))


def test_data_class():
    # what we expect to get
    expected: Class = Class(
        name="DataClass",
        attributes=Attributes(
            attributes=[Attribute(name="name", dtype=String()), Attribute(name="active", dtype=Boolean())]
        ),
        is_dataclass=True,
        inherits_from=[],
    )

    created = Class.from_ast(class_def=class_definitions[0])

    assert created == expected


def test_sequences():
    # what we expect to get
    expected: Class = Class(
        name="Sequences",
        attributes=Attributes(
            attributes=[
                Attribute(name="names", dtype=List([String()])),
                Attribute(name="numbers", dtype=Tuple([Integer(), Integer()])),
                Attribute(name="pairs", dtype=Dict([String(), String()])),
                Attribute(name="set_int", dtype=Set([Integer()])),
            ]
        ),
        is_dataclass=True,
        inherits_from=[],
    )

    created = Class.from_ast(class_def=class_definitions[1])

    assert created == expected


def test_nested_annotation():
    # expected annotations
    name_annotation = List([Dict([Tuple([Integer(), String()]), List([String()])])])
    arg_annotation = Dict([Tuple([Tuple([Integer(), String()]), List([String()])]), List([Integer()])])

    # what we expect to get
    expected: Class = Class(
        name="Nested",
        attributes=Attributes(attributes=[Attribute(name="name", dtype=name_annotation)]),
        is_dataclass=True,
        inherits_from=[],
        functions=[
            Function(name="greet", parameters=[Parameter(name="arg", dtype=arg_annotation)], return_type=String())
        ],
        classes=[],
    )

    created = Class.from_ast(class_def=class_definitions[2])

    assert created == expected


def test_missing_annotation():
    expected: Class = Class(
        name="MissingAnnotation",
        attributes=Attributes(
            attributes=[
                Attribute(name="name", dtype=Undefined()),
            ]
        ),
        is_dataclass=False,
        inherits_from=[],
        functions=[Function(name="return_without_type", parameters=[], return_type=Undefined())],
    )

    created = Class.from_ast(class_def=class_definitions[3])

    assert created == expected


def test_complex_assignments():
    expected: Class = Class(
        name="ComplexAssignments",
        attributes=Attributes(
            attributes=[
                Attribute(name="first", dtype=Undefined()),
                Attribute(name="second", dtype=Undefined()),
                Attribute(name="third", dtype=Undefined()),
            ]
        ),
        is_dataclass=False,
        inherits_from=[],
        functions=[Function(name="return_tuples", parameters=[], return_type=Undefined())],
    )

    created = Class.from_ast(class_def=class_definitions[4])

    assert created == expected


test_nested_annotation()
