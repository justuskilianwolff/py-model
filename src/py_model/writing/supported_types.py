from enum import Enum

from .graphs.graph_writer import DotWriter
from .languages.language_writer import TypeScriptWriter


class SupportedTypes(Enum):
    ts = TypeScriptWriter()
    dot = DotWriter()
