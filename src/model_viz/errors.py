class NotImplementedError(NotImplementedError):
    def __init__(
        self,
        message: str = "Please raise an issue with a minimal working example at https://github.com/justuskilianwolff/model-viz",
    ) -> None:
        self.message = message
        super().__init__(message)
