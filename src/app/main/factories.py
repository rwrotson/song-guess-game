from app.abstract.validators import Validator
from app.abstract.processors import Processor
from app.abstract.presenters import Presenter
from app.abstract.menus import Menu
from app.main.state import State, Stage
from app.cli.factories import menu_info_factory, menu_factory
from app.settings.factories import settings_factory


def menu_model_factory(state: State) -> Menu:
    stage = state.stage
    if stage in Stage.MAIN_SETTINGS | Stage.ADVANCED_SETTINGS:
        menu_info = settings_factory(stage)
    else:
        menu_info = menu_info_factory(stage)
    return menu_factory(menu_info)


def validator_factory(state: State) -> Validator:
    return


def processor_factory() -> Processor:
    return


def presenter_factory() -> Presenter:
    return


def menu_info_factory(stage: Stage) -> type[structs.MenuTemplate]:
    mapping = {
        Stage.MAIN.MAIN_MENU: structs.MainMenu,
        Stage.MAIN.SETTINGS: structs.SettingsMenu,
        Stage.MAIN.README: structs.ReadmeMenu,
        Stage.SETTINGS_SECTIONS.MAIN_SETTINGS: structs.MainSettingsMenu,
        Stage.SETTINGS_SECTIONS.ADVANCED_SETTINGS: structs.AdvancedSettingsMenu,
        Stage.GAME.QUESTION: structs.QuestionMenu,
        Stage.GAME.ANSWER: structs.AnswerMenu,
        Stage.GAME.EVALUATION: structs.EvaluationMenu,
        Stage.GAME.ENDGAME: "add",
    }

    return mapping[stage]