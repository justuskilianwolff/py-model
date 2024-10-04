import ast


class AssignVisitor(ast.NodeVisitor):
    """Visitor to find all assignments (annotated and not annotated) in a class."""

    def __init__(self):
        self.ann_assigns: list[ast.AnnAssign] = []
        self.assigns: list[ast.Assign] = []

    def visit_AnnAssign(self, node: ast.AnnAssign):
        self.ann_assigns.append(node)

    def visit_Assign(self, node: ast.Assign):
        self.assigns.append(node)


class OuterAssignVisitor(AssignVisitor):
    """Visitor to find all assignments in a class but not within a subclasses."""

    def __init__(self, class_name: str):
        self.class_name = class_name

        super().__init__()

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == self.class_name:
            super().generic_visit(node)
        else:
            pass
