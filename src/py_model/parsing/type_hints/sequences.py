from py_model.parsing import BuildingBlock

from .basic_types import TypeHint


class SingleContainer(TypeHint, BuildingBlock):
    """A container that can hold a single dtype"""

    def __init__(self, dtype: list[TypeHint] | TypeHint | None = None) -> None:
        if isinstance(dtype, list):
            if len(dtype) != 1:
                raise ValueError("SingleContainer must have exactly one type hint (or None)")
            else:
                self.dtype = dtype[0]
        else:
            self.dtype = dtype

    def __str__(self) -> str:
        container = self.__class__.__name__.lower()
        if self.dtype is None:
            return container
        else:
            return f"{container}[{self.dtype}]"


class DoubleContainer(TypeHint, BuildingBlock):
    """ "can excatlly hold two dtypes"""

    def __init__(self, dtypes: list[TypeHint] | None = None) -> None:
        if (dtypes is not None) and (len(dtypes) != 2):
            raise ValueError("DoubleContainer must have exactly two type hints (or None)")

        self.dtypes = dtypes

    def __str__(self) -> str:
        container = self.__class__.__name__.lower()
        if self.dtypes is None:
            return container
        else:
            return f"{container}[{self.dtypes[0]}, {self.dtypes[1]}]"


class MultipleContainer(TypeHint, BuildingBlock):
    """Can hold many dtypes"""

    def __init__(self, dtypes: list[TypeHint] | None = None) -> None:
        self.dtypes = dtypes

    def __str__(self) -> str:
        container = self.__class__.__name__.lower()
        if self.dtypes is None:
            return container
        else:
            return f"{container}[{', '.join([str(dtype) for dtype in self.dtypes])}]"


class Tuple(MultipleContainer):
    def typescript(self) -> str:
        if self.dtypes is None:
            raise ValueError("Tuple must have at least one type hint for conversion to Typescript.")
        else:
            return f"[{', '.join(dtype.typescript() for dtype in self.dtypes)}]"


class List(SingleContainer):
    def typescript(self) -> str:
        if self.dtype is None:
            raise ValueError("List must have at least one type hint for conversion to Typescript.")
        else:
            return f"Array<{self.dtype.typescript()}>"


class Dict(DoubleContainer):
    def typescript(self) -> str:
        if self.dtypes is None:
            raise ValueError("Dict must have type hints for conversion to Typescript.")
        else:
            return f"Map<{self.dtypes[0].typescript()}, {self.dtypes[1].typescript()}>"


class Set(SingleContainer):
    def typescript(self) -> str:
        if self.dtype is None:
            raise ValueError("Set must have type hints for conversion to Typescript.")
        else:
            return f"Set<{self.dtype.typescript()}>"


class Union(TypeHint):
    """A class that represents a union of data types."""

    def __init__(self, dtypes: list[TypeHint]) -> None:
        if (dtypes is None) or (len(dtypes) < 2):
            raise ValueError("Union must have at least two type hints.")

        self.dtypes = dtypes

    def __str__(self) -> str:
        return f"{' | '.join(str(dtype) for dtype in self.dtypes)}"
