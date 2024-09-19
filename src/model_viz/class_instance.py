import ast

from .string_repr import get_attr_repr, get_func_repr


class ClassInstance:
    def __init__(self, cls: ast.ClassDef, filepath: str | None = None):
        # in case of multiple files with same class definitison
        # import_path = filepath.replace(os.path.sep, ".").replace(".py", "") + "." if filepath else "" #TODO: fix
        self.class_name: str = cls.name
        self.inherits_from: list[ast.Name] = self.get_inheritance(cls)
        self.functions: list[ast.FunctionDef] = [f for f in self.get_functions(cls) if f.name != "__init__"]
        self.attributes: list[ast.AnnAssign | ast.Assign] = self.get_attributes(cls)

    def __str__(self) -> str:
        name = self.class_name
        inheritance = "inheritance: " + ", ".join([inh.id for inh in self.inherits_from])
        functions = "functions: " + ", ".join([get_func_repr(func) for func in self.functions])
        attributes = "attributes: " + ", ".join([get_attr_repr(attr) for attr in self.attributes])
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
            elif isinstance(body_item, ast.FunctionDef):
                for element in body_item.body:
                    if isinstance(element, ast.Assign) or isinstance(element, ast.AnnAssign):
                        attributes.append(element)

        return attributes
