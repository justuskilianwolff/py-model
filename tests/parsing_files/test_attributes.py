import ast

from py_model.datatypes import String, Undefined
from py_model.types import Attribute


def test_creation_attribute():
    # we excpet no error
    Attribute(name="name", dtype=String())


def test_handle_annotated_assign():
    # create annassign
    ann_assign = "x: str = 'hello'"

    # get the node
    node = ast.parse(ann_assign).body[0]

    assert isinstance(node, ast.AnnAssign)

    # create the attribute
    created = Attribute.handle_annotated_assignment(node=node)
    expected = Attribute(name="x", dtype=String())

    assert created == expected


def test_handle_assign():
    # create assign
    assign = "self.x = 'hello'"

    # get the node
    node = ast.parse(assign).body[0]

    assert isinstance(node, ast.Assign)

    # create the attribute
    created = Attribute.handle_assign(node=node)[0]
    expected = Attribute(name="x", dtype=Undefined())

    assert created == expected
