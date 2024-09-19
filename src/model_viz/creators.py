from abc import ABC, abstractmethod


class Creator(ABC):
    @property
    def inherited_property(self):
        return "Creator"

    @property
    @abstractmethod
    def relation(self):
        pass


class DotCreator(Creator):
    @property
    def relation(self):
        return "-->"
