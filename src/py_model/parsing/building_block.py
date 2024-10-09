from abc import ABC, abstractmethod
from py
class BuilduingBlock(ABC):
    @abstractmethod
    def get_string(self):
        return self.__str__()