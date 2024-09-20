import ast

from model_viz.logging import get_logger

from ..utils import OuterGeneralAssignVisitor
from . import Attribute, Attributes, Function

logger = get_logger(__name__)


class ClassInstance:
    def __init__(self, cls: ast.ClassDef, filepath: str | None = None):
        # in case of multiple files with same class definitison
        # import_path = filepath.replace(os.path.sep, ".").replace(".py", "") + "." if filepath else "" #TODO: fix
        self.class_name: str = cls.name
        self.inherits_from: list[str] = self.get_inheritance(cls)
        self.functions: list[Function] = self.get_functions(cls)
        self.attributes: Attributes = self.get_attributes(cls)

    def __str__(self) -> str:
        name = self.class_name
        inheritance = "inheritance: " + ", ".join([inh for inh in self.inherits_from])
        functions = "functions: " + ", ".join([str(func) for func in self.functions])
        attributes = "attributes: " + str(self.attributes)
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

    def get_attributes(self, cls: ast.ClassDef) -> Attributes:
        """Find all self. attributes in a class.

        Args:
            cls (ast.ClassDef): _description_

        Returns:
            list[Attribute]: _description_
        """

        # store attributes
        attributes = Attributes(attributes=[])

        # check whether class is a dataclass
        is_dc = "dataclass" in [dec.id for dec in cls.decorator_list]

        if is_dc:
            # iterate over all fields in the dataclass
            to_remove = []  # remove ann assigns from class body so they are not visited again later
            for body_item in cls.body:
                if isinstance(body_item, ast.AnnAssign):
                    attribute = Attribute.handle_ann_assign(body_item, is_dc=is_dc)
                    if attribute is not None:
                        attributes.add_attribute(attribute=attribute)

                    # remove the attribute from the class body
                    to_remove.append(body_item)
                else:
                    # no more variable definitions in datclass 'style'
                    break
            for item in to_remove:
                cls.body.remove(item)

        # visit all assign and ann_assign nodes in the class body but not within a nested class
        # FIXME: create a innerclass list andn then recursively visit
        general_assign_visitor = OuterGeneralAssignVisitor(class_name=cls.name)
        general_assign_visitor.visit(cls)

        # handle ann asigns first
        for node in general_assign_visitor.ann_assigns:
            attribute = Attribute.handle_ann_assign(
                node, is_dc=False
            )  # cant be a dataclass declaration since already handled
            if attribute is not None:
                attributes.add_attribute(attribute=attribute)

        # handle assigns
        for node in general_assign_visitor.assigns:
            attributes.add_attributes(attributes=Attribute.handle_assign(node))

        return attributes
