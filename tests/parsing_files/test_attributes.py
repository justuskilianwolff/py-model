import ast

from py_model.datatypes import String, Undefined
from py_model.building_blocks import Attribute, Attributes


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
