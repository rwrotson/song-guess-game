from dataclasses import dataclass
from enum import StrEnum, auto

from app.abstract.presenters import Presenter
from app.game.presenters import (
    AnswerPresenter,
    ScorePresenter,
    EvaluationPresenter,
    QuestionPresenter,
)
from app.readme.presenters import ReadmePresenter
from app.settings.models import Settings
from app.settings.presenters import (
    MainSettingsPresenter,
    AdvancedSettingsPresenter,
)
from app.utils import get_singleton_instance


class Stage(StrEnum):
    MAIN_MENU = auto()
    SETTINGS_MENU = auto()
    MAIN_SETTINGS = auto()
    ADVANCED_SETTINGS = auto()
    READY_TO_PLAY = auto()
    README = auto()


class GameStage(StrEnum):
    QUESTION = auto()
    ANSWER = auto()
    EVALUATION = auto()
    ENDGAME = auto()


@dataclass(slots=True)
class GameState:
    current_user_id: int = 0
    current_round: int = 1


@dataclass(slots=True)
class _State:
    stage: Stage | GameStage = Stage.MAIN_MENU
    game: GameState = GameState()
    settings: Settings = Settings()


def get_state() -> _State:
    return get_singleton_instance(cls=_State)


def presenter_factory(state: State) -> Presenter:
    mapping = {
        Stage.MAIN_MENU: MainMenuPresenter,
        Stage.MAIN_SETTINGS: MainSettingsPresenter,
        Stage.ADVANCED_SETTINGS: AdvancedSettingsPresenter,
        Stage.README: ReadmePresenter,
        GameStage.QUESTION: QuestioningPresenter,
        GameStage.ANSWER: AnsweringPresenter,
        GameStage.EVALUATION: EvaluatingPresenter,
        GameStage.ENDGAME: EndgamePresenter,
    }
    raise ValueError(f"Invalid stage: {state.stage}")



