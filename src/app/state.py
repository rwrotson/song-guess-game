from enum import Enum, StrEnum, auto

from app.game.models import Game
from app.settings.models import Settings, DisplaySettings
from app.viewers import ViewersContainer
from app.utils import get_singleton_instance


class Stage(Enum):
    class MAIN(StrEnum):
        MAIN_MENU = auto()
        SETTINGS = auto()
        README = auto()

    class SETTINGS(StrEnum):
        MAIN_SETTINGS = auto()
        ADVANCED_SETTINGS = auto()

    class GAME(StrEnum):
        QUESTION = auto()
        ANSWER = auto()
        EVALUATION = auto()
        ENDGAME = auto()


class State:
    __slots__ = ("stage", "settings", "viewers", "game")

    def __init__(self):
        self.stage = Stage.MAIN.MAIN_MENU
        self.settings: Settings = Settings.load_from_file()
        self.viewers = ViewersContainer(
            display_settings=self.settings.display,
            players_number=self.settings.players_number,
        )
        self.game: Game | None = None

    def restart_game(self) -> None:
        self.stage = Stage.GAME.QUESTION
        self.game = Game(players=self.settings.players, rounds=self.settings.rounds)

    def resume_game(self) -> None:
        self.stage = Stage.GAME.QUESTION
        self.game = Game.from_pickle()

    def exit_game(self) -> None:
        import sys

        self.game.pickle()

        viewer = self.viewers.default_viewer
        viewer.display("Bye! See you soon!")

        sys.exit()


def get_state() -> State:
    return get_singleton_instance(cls=State)
