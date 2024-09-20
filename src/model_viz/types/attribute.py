from model_viz.utils import indicate_access_level

from . import TypeHintableValue


class Attribute(TypeHintableValue):
    def __str__(self) -> str:
        return indicate_access_level(super().__str__())
