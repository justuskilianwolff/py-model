class MissingImplementationError(NotImplementedError):
    def __init__(
        self,
        message: str | None = None,
    ) -> None:
        base_message = "Please raise an issue with a minimal (not) working example at https://github.com/justuskilianwolff/py-model"
        if message:
            text = f"{base_message}: {message}"
        else:
            text = base_message
        super().__init__(text)
