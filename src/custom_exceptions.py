class ConflictException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class WrongDataTypeException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class MissingFieldException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
