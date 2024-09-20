from model_viz.utils import indicate_access_level

from .parameter import Parameter


class Function:
    def __init__(self, name: str, parameters: list[Parameter], return_type: str | None) -> None:
        self.name = name
        self.parameters = parameters
        self.return_type = return_type

    def __str__(self) -> str:
        str_representation = f"{self.name}({', '.join([str(param) for param in self.parameters])})"
        if self.return_type is not None:
            str_representation += f" -> {self.return_type}"
        return indicate_access_level(str_representation)
