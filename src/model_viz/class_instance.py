import ast
import os

from .printers import print_attribute, print_function


class ClassInstance:
    def __init__(self, cls: ast.ClassDef, filepath: str | None = None):
        # in case of multiple files with same class definitison
        import_path = filepath.replace(os.path.sep, ".").replace(".py", "") + "." if filepath else ""
        self.class_name: str = import_path + cls.name
        self.inherits_from: list[ast.Name] = self.get_inheritance(cls)
        self.functions: list[ast.FunctionDef] = [f for f in self.get_functions(cls) if f.name != "__init__"]
        self.attributes: list[ast.AnnAssign | ast.Assign] = self.get_attributes(cls)

    def __str__(self) -> str:
        name = self.class_name
        inheritance = "inheritance: " + ", ".join([inh.id for inh in self.inherits_from])
        functions = "functions: " + ", ".join([print_function(func) for func in self.functions])
        attributes = "attributes: " + ", ".join([print_attribute(attr) for attr in self.attributes])
        return f"{name}: {inheritance}; {functions}; {attributes}"

    def get_inheritance(self, cls: ast.ClassDef) -> list[ast.Name]:
        inherits_from = []
        for base in cls.bases:
            if isinstance(base, ast.Name):
                inherits_from.append(base)
        # TODO: how are we going to handle import issues like renaming: import x as y?
        return inherits_from

    def get_functions(self, cls: ast.ClassDef) -> list[ast.FunctionDef]:
        functions = []
        for body_item in cls.body:
            if isinstance(body_item, ast.FunctionDef):
                # using custom class to overwrite __str__ method
                functions.append(body_item)
        return functions

    def get_attributes(self, cls: ast.ClassDef) -> list[ast.AnnAssign | ast.Assign]:
        attributes = []
        for body_item in cls.body:
            if isinstance(body_item, ast.AnnAssign) or isinstance(body_item, ast.Assign):
                attributes.append(body_item)

        return attributes

    # def set_attributes(self, cls: ast.ClassDef):
    #     class_details = {}

    #     class_name = cls.name
    #     class_attributes = set()
    #     instance_attributes = set()

    #     # Examine class body
    #     for body_item in cls.body:
    #         # Class attributes (direct assignments)
    #         if isinstance(body_item, ast.Assign):
    #             for target in body_item.targets:
    #                 if isinstance(target, ast.Name):
    #                     class_attributes.add(target.id)

    #         # Class attributes (properties and class methods)
    #         elif isinstance(body_item, ast.FunctionDef):
    #             if body_item.decorator_list:
    #                 for decorator in body_item.decorator_list:
    #                     if isinstance(decorator, ast.Name) and decorator.id in ["classmethod", "classproperty"]:
    #                         class_attributes.add(body_item.name)

    #         # Instance attributes
    #         if isinstance(body_item, ast.FunctionDef):
    #             for stmt in body_item.body:
    #                 if isinstance(stmt, ast.Assign):
    #                     for target in stmt.targets:
    #                         if (
    #                             isinstance(target, ast.Attribute)
    #                             and isinstance(target.value, ast.Name)
    #                             and target.value.id == "self"
    #                         ):
    #                             instance_attributes.add(target.attr)

    #     # Examine class decorators
    #     for decorator in cls.decorator_list:
    #         if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
    #             if decorator.func.id == "dataclass":
    #                 # For dataclasses, all fields are considered class attributes
    #                 for field in cls.body:
    #                     if isinstance(field, ast.AnnAssign) and isinstance(field.target, ast.Name):
    #                         class_attributes.add(field.target.id)

    #     class_details[class_name] = {
    #         "class_attributes": list(class_attributes),
    #         "instance_attributes": list(instance_attributes),
    #     }

    #     return class_details
