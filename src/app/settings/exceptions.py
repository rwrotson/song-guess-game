from app.exceptions import SongRouletteError


class SettingsHaveNotBeenSet(SongRouletteError):
    """
    Exception raised when settings have not been set.
    """
    pass


class SettingsValidationError(SongRouletteError):
    """
    Exception raised when settings are invalid.
    """
    pass


class SettingsFileNotFoundError(SongRouletteError):
    """
    Exception raised when settings file is not found.
    """
    pass


class SettingsSectionNotFoundError(SongRouletteError):
    """
    Exception raised when settings section is not found.
    """
    pass
