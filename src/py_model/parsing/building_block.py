from abc import ABC, abstractmethod

from py_model.writing import SupportedTypes


class BuildingBlock(ABC):
    """Lists all supported types and provides a method to get the string representation
    of the object in the desired format"""

    @abstractmethod
    def typescript(self) -> str:
        pass

    @abstractmethod
    def dot(self) -> str:
        pass

    def get_string(self, supported_type: SupportedTypes) -> str:
        if supported_type == SupportedTypes.ts:
            return self.typescript()
        elif supported_type == SupportedTypes.dot:
            return self.dot()
