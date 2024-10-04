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

    def __init__(self, dtypes: list[DataType]) -> None:
        self.dtypes = dtypes


class BaseSequence(DataType, Sequence):
    def __init__(self, dtypes: list[DataType] | DataType | None = None) -> None:
        if isinstance(dtypes, DataType):
            dtypes = [dtypes]
        super().__init__(dtypes)


class Tuple(BaseSequence):
    pass


class List(BaseSequence):
    pass


class Dict(BaseSequence):
    pass


class Set(BaseSequence):
    pass


class Union(NotEmptySequence, DataType):
    """A class that represents a union of data types."""

    def __init__(self, dtypes: list[DataType]) -> None:
        super().__init__(dtypes)

    def __str__(self) -> str:
        return f"{' | '.join(str(dtype) for dtype in self.dtypes)}"
