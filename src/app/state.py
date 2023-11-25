from dataclasses import dataclass
from enum import StrEnum, auto


@dataclass(slots=True)
class SettingsState:
    pass


class GameStage(StrEnum):
    NOT_STARTED = auto()
    QUESTIONING = auto()
    ANSWERING = auto()
    EVALUATING = auto()


@dataclass(slots=True)
class GameState:
    current_user_id: int = 0
    current_round: int = 1
    current_stage: GameStage = GameStage.NOT_STARTED


class Stage(StrEnum):
    MAIN_MENU = auto()
    SETTINGS = auto()
    GAME = auto()
    README = auto()


@dataclass(slots=True)
class State:
    stage: Stage = Stage.MAIN_MENU
    game: GameState = GameState()
    settings: SettingsState = SettingsState()
    readme: ReadmeState = ReadmeState()
