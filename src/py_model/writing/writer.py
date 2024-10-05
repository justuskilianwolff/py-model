from dataclasses import dataclass


@dataclass
class Writer:
    text: str = ""

    def write(self, file_path: str):
        with open(file_path, "w") as file:
            file.write(self.text)
