from dataclasses import dataclass

from py_model.navigation import get_classes
from py_model.parsing import Class


@dataclass
class Writer:
    needs_annotation: bool = False  # whether a writer needs an annotation to convert (e.g. TypeScript)
    text: str = ""

    def parse_classes(self, file_paths: list[str]) -> list[Class]:
        class_instances: list[Class] = list()

        for filepath in sorted(file_paths):
            classes = get_classes(filepath)

            # create class instances
            for cls in classes:
                class_instance = Class.from_ast(cls, needs_annotation=self.needs_annotation)
                class_instances.append(class_instance)

        return class_instances

    def write(self, file_path: str):
        with open(file_path, "w") as file:
            file.write(self.text)
