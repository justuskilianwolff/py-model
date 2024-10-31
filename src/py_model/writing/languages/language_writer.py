from ..writer import Writer


class LanguageWriter(Writer):
    pass


class TypeScriptWriter(LanguageWriter):
    def __init__(self):
        super().__init__(needs_annotation=True)
