from .basic_types import DataType


class Sequence:
    """A class that represents a sequence of data types."""

    def __init__(self, dtypes: list[DataType] | None = None) -> None:
        self.dtypes = dtypes

    def __str__(self) -> str:
        container = self.__class__.__name__.lower()
        if self.dtypes is None:
            return container
        else:
            return f'{container}[{", ".join(str(dtype) for dtype in self.dtypes)}]'


class NotEmptySequence(Sequence):
    """A class that represents a sequence of data types that is not empty."""

    def __init__(self, dtypes: list[DataType | str]) -> None:
        self.dtypes = dtypes


class Tuple(DataType, Sequence):
    def __init__(self, dtypes: list[DataType] | None = None) -> None:
        super().__init__(dtypes)


class List(DataType, Sequence):
    def __init__(self, dtypes: list[DataType] | None = None) -> None:
        super().__init__(dtypes)


class Union(NotEmptySequence, DataType):
    """A class that represents a union of data types."""

    def __init__(self, dtypes: list[DataType | str]) -> None:
        super().__init__(dtypes)

    def __str__(self) -> str:
        return f"{' | '.join(str(dtype) for dtype in self.dtypes)}"
