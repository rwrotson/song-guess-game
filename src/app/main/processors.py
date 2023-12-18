from abc import ABC, abstractmethod

from app.main.state import Stage, State, get_state


class Processor(ABC):
    """
    Class that processes user input and changes app state due to user's command.
    """
    __slots__ = ("_state", "_model")

    def __init__(self):
        self._state: State = get_state()

    @abstractmethod
    def process(self, input_text: str, /) -> None:
        ...


class MainMenuProcessor(Processor):
    def process(self, input_text: str, /) -> None:
        match input_text:
            case "1" | "PLAY":
                self._state.restart_game()
            case "2" | "SETTINGS":
                self._state.stage = Stage.MAIN.SETTINGS
            case "3" | "README":
                self._state.stage = Stage.MAIN.README
            case "4" | "EXIT":
                self._state.exit_game()
            case _:
                raise ValueError("Invalid input.")


class SettingsProcessor(Processor):
    def process(self, input_text: str, /) -> None:
        match input_text:
            case "1" | "MAIN SETTINGS":
                self._state.stage = Stage.SETTINGS_SECTIONS.MAIN_SETTINGS
            case "2" | "ADVANCED SETTINGS":
                self._state.stage = Stage.SETTINGS_SECTIONS.ADVANCED_SETTINGS
            case "3" | "SHOW CURRENT SETTINGS":
                self._state.stage = Stage.SETTINGS.SHOW_CURRENT_SETTINGS
            case "4" | "EDIT CONFIG FILE":
                self._state.stage = Stage.SETTINGS.EDIT_CONFIG_FILE
            case "5" | "BACK":
                self._state.stage = Stage.MAIN.MAIN_MENU
            case _:
                raise ValueError("Invalid input.")


class MainSettingsProcessor(Processor):
    def process(self, input_text: str, /) -> None:
        match input_text:
            case "1" | "GAME SETTINGS":
                self._state.stage = Stage.MAIN_SETTINGS.GAME_SETTINGS
            case "2" | "PLAYER SETTINGS":
                self._state.stage = Stage.MAIN_SETTINGS.PLAYER_SETTINGS
            case "3" | "BACK":
                self._state.stage = Stage.MAIN.MAIN_MENU
            case _:
                raise ValueError("Invalid input.")