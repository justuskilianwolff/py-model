from __future__ import annotations

import ast

# from .class_definition import Class
# from .function import Function



class Instance:
    """Parent of Function and Class"""

    def __init__(self, definition: ast.ClassDef | ast.FunctionDef):
        # set those when walking the body
        self.functions: list=[]
        self.classes: list=[]
        
        self.definition = definition

    def walk_body(self):
        pass
        # for body_item in self.body:
        #     if isinstance(body_item, ast.FunctionDef):
        #         self.functions.append(func)

        #     if isinstance(body_item, ast.ClassDef):
        #         class_instance = Class(cls=body_item)
        #         self.classes.append(class_instance)
