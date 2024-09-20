import ast

from model_viz.logging import get_logger

logger = get_logger(__name__)


def vulture_ignore(obj):
    """Decorator to ignore vulture warnings for a function."""
    return obj


def indicate_access_level(name: str) -> str:
    """Indicate access level of a class, function or attribute."""

    if name.startswith("__"):
        # double underscore indicates private
        return "-" + name[2:]
    elif name.startswith("_"):
        # single underscore indicates protected
        return "#" + name[1:]
    else:
        # no underscore indicates public
        return "+" + name


class OuterGeneralAssignVisitor(ast.NodeVisitor):
    def __init__(self, class_name: str):
        self.ann_assigns: list[ast.AnnAssign] = []
        self.assigns: list[ast.Assign] = []
        self.inside_class = False
        self.class_name = class_name

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == self.class_name:
            super().generic_visit(node)
        else:
            pass

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if not self.inside_class:
            self.ann_assigns.append(node)

    def visit_Assign(self, node: ast.Assign):
        if not self.inside_class:
            self.assigns.append(node)
