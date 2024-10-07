from .basic_types import TypeHint


class TypeHintSequence(TypeHint):
    """A class that represents a typehint than can hold a list of type hints."""

    def __init__(self, dtypes: list[TypeHint] | TypeHint | None = None) -> None:
        if isinstance(dtypes, TypeHint):
            dtypes = [dtypes]

        self.dtypes = dtypes

    def __str__(self) -> str:
        container = self.__class__.__name__.lower()
        if self.dtypes is None:
            return container
        else:
            return f'{container}[{", ".join(str(dtype) for dtype in self.dtypes)}]'


class Tuple(TypeHintSequence):
    pass


class List(TypeHintSequence):
    pass


class Dict(TypeHintSequence):
    pass


class Set(TypeHintSequence):
    pass


class Union(TypeHint):
    """A class that represents a union of data types."""

    def __init__(self, dtypes: list[TypeHint]) -> None:
        if (dtypes is None) or (len(dtypes) < 2):
            raise ValueError("Union must have at least two type hints.")

        self.dtypes = dtypes

    def __str__(self) -> str:
        return f"{' | '.join(str(dtype) for dtype in self.dtypes)}"
