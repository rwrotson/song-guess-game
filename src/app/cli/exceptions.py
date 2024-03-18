from app.exceptions import SongRouletteError


class IncorrectMenuConfigurationError(SongRouletteError):
    """
    Raised when wrong menu type is passed to the factory, function or method.
    """
    pass


class InvalidInputError(SongRouletteError):
    """
    Exception raised when an input is invalid.
    """
    pass
