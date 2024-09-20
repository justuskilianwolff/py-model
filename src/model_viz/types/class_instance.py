import ast

from model_viz.logging import get_logger

from ..utils import OuterGeneralAssignVisitor
from . import Attribute, Function

logger = get_logger(__name__)


class ClassInstance:
    def __init__(self, cls: ast.ClassDef, filepath: str | None = None):
        # in case of multiple files with same class definitison
        # import_path = filepath.replace(os.path.sep, ".").replace(".py", "") + "." if filepath else "" #TODO: fix
        self.class_name: str = cls.name
        self.inherits_from: list[str] = self.get_inheritance(cls)
        self.functions: list[Function] = self.get_functions(cls)
        self.attributes: list[Attribute] = self.get_attributes(cls)

    def __str__(self) -> str:
        name = self.class_name
        inheritance = "inheritance: " + ", ".join([inh for inh in self.inherits_from])
        functions = "functions: " + ", ".join([str(func) for func in self.functions])
        attributes = "attributes: " + ", ".join([str(attr) for attr in self.attributes])
        return f"{name}: {inheritance}; {functions}; {attributes}"

    def get_inheritance(self, cls: ast.ClassDef) -> list[str]:
        inherits_from = []
        for base in cls.bases:
            if isinstance(base, ast.Name):
                inherits_from.append(base.id)
        # TODO: how are we going to handle import issues like renaming: import x as y?
        return inherits_from

    def get_functions(self, cls: ast.ClassDef) -> list[Function]:
        functions = []
        for body_item in cls.body:
            if isinstance(body_item, ast.FunctionDef):
                func = Function.create_function(func=body_item)

                # skip __init__ method
                if func.name == "__init__":
                    continue

                functions.append(func)

        return functions

    def get_attributes(self, cls: ast.ClassDef) -> list[Attribute]:
        """Find all self. attributes in a class.

        Args:
            cls (ast.ClassDef): _description_

        Returns:
            list[Attribute]: _description_
        """

        def handle_ann_assign(node: ast.AnnAssign, is_dc: bool) -> Attribute | None:
            # obtain name
            if isinstance(node.target, ast.Attribute):
                # happens when
                name = node.target.attr
            elif isinstance(node.target, ast.Name):
                name = node.target.id
            else:
                raise NotImplementedError()

            if not is_dc:
                # if it is not a dataclass, the attribute should start with 'self.'
                if isinstance(node.target, ast.Attribute):
                    if node.target.value.id != "self":
                        return None

            # get annotation
            if isinstance(node.annotation, ast.Name):
                type = node.annotation.id
            elif isinstance(node.annotation, ast.Subscript):
                type = node.annotation.value.id
            else:
                type = None
            return Attribute(name=name, type=type)

        def handle_assign(node: ast.Assign) -> list[Attribute]:
            attributes = []
            for target in node.targets:
                # check that this actually is a self. attribute
                if isinstance(target, ast.Attribute):
                    if target.value.id != "self":
                        continue

                    name = target.attr

                    # add attribute to list
                    attributes.append(Attribute(name=name, type=None))

            return attributes

        # store attributes
        attributes = []

        # check whether class is a dataclass
        is_dc = "dataclass" in [dec.id for dec in cls.decorator_list]

        if is_dc:
            # iterate over all fields in the dataclass
            to_remove = []  # remove ann assigns from class body so they are not visited again later
            for body_item in cls.body:
                if isinstance(body_item, ast.AnnAssign):
                    attribute = handle_ann_assign(body_item, is_dc=is_dc)
                    attributes.append(attribute)

                    # remove the attribute from the class body
                    to_remove.append(body_item)
                else:
                    # no more variable definitions in datclass 'style'
                    break
            for item in to_remove:
                cls.body.remove(item)

        # visit all assign and ann_assign nodes in the class body but not within a nested class
        general_assign_visitor = OuterGeneralAssignVisitor(
            class_name=cls.name
        )  # FIX: create a innerclass list andn then recursively visit
        general_assign_visitor.visit(cls)

        # handle ann asigns first
        for node in general_assign_visitor.ann_assigns:
            attribute = handle_ann_assign(node, is_dc=False)  # cant be a dataclass declaration since already handled
            if attribute is not None:
                attributes.append(attribute)

        # handle assigns
        for node in general_assign_visitor.assigns:
            attributes += handle_assign(node)

        return attributes
