class SongRouletteError(Exception):
    """
    Base class for exceptions in this project.
    """
    pass


class NotSupportedFormatError(SongRouletteError):
    """
    Exception raised when a file format is not supported.
    """
    pass


class InvalidConfigFileError(SongRouletteError):
    """
    Exception raised when a config file is invalid.
    """
    pass


class InvalidGameFileError(SongRouletteError):
    """
    Exception raised when a game file is invalid.
    """
    pass
