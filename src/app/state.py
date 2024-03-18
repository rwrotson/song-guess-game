from enum import Enum, StrEnum, auto, member
from typing import Any

from app.game.models import Game
from app.settings.models import get_settings, Settings
from app.viewers import AppViewer
from app.utils import get_singleton_instance


class Stage(Enum):
    MAIN_MENU = auto()
    README = auto()
    LIBRARIES_STATS = auto()

    @member
    class SETTINGS(StrEnum):
        ALL_SETTINGS = auto()
        MAIN_SETTINGS = auto()
        ADVANCED_SETTINGS = auto()
        PLAYERS = auto()

    @member
    class MAIN_SETTINGS(StrEnum):
        GAME = auto()
        PLAYER = auto()

    @member
    class ADVANCED_SETTINGS(StrEnum):
        DISPLAY = auto()
        SELECTION = auto()
        SAMPLING = auto()
        PLAYBACK_BAR = auto()
        EVALUATION = auto()
        SERVICE_PATHS = auto()

    @member
    class GAME(StrEnum):
        QUESTION = auto()
        ANSWER = auto()
        EVALUATION_ = auto()
        ENDGAME = auto()


class State:
    __slots__ = ("_stage", "_previous_stage", "_settings", "_game", "_viewer", "data")

    def __init__(self):
        self._stage: Stage = Stage.MAIN_MENU
        self._previous_stage: Stage | None = None
        self._settings: Settings = get_settings().load_from_file()
        self._game: Game = Game.from_settings()
        self.data: dict[str, Any] = {}

        self._viewer = AppViewer()

    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, new_stage: Stage):
        self._previous_stage = self._stage
        self._stage = new_stage

    @property
    def previous_stage(self):
        return self._previous_stage

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def game(self) -> Game | None:
        return self._game

    @property
    def viewer(self) -> AppViewer:
        return self._viewer

    def restart_game(self) -> None:
        self._game.initialize_songs()
        self._game.status = "in_progress"
        self._viewer = self._viewer.refreshed()
        self.stage = Stage.GAME.value.QUESTION

    def resume_game(self) -> None:
        self._game = Game.from_pickle()
        self._viewer = self._viewer.refreshed()
        self.stage = Stage.GAME.value.QUESTION

    def exit_game(self) -> None:
        import sys

        # self.game.pickle()

        self.viewer.display("Bye! See you soon!")

        sys.exit()


def get_state() -> State:
    return get_singleton_instance(cls=State)
