from ..writer import Writer


class GraphWriter(Writer):
    post_text: str = ""  # Holds the arrows to be added to the end of the text

    def write(self, file_path: str):
        with open(file_path, "w") as file:
            file.write(self.text + self.post_text)


class DotWriter(GraphWriter):
    pass
