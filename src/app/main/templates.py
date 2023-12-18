from enum import auto

from app.cli.templates import MenuTemplate
from app.utils import classproperty


class MainMenu(MenuTemplate):
    PLAY = auto()
    SETTINGS = auto()
    README = auto()
    EXIT = auto()

    @classproperty
    def prompt(self) -> str:
        return "Select main menu section:"


class SettingsMenu(MenuTemplate):
    MAIN_SETTINGS = auto()
    ADVANCED_SETTINGS = auto()
    SHOW_CURRENT_SETTINGS = auto()
    EDIT_CONFIG_FILE = auto()
    BACK = auto()

    @classproperty
    def prompt(self) -> str:
        return "Select settings menu section:"


class MainSettingsMenu(MenuTemplate):
    GAME_SETTINGS = auto()
    PLAYER_SETTINGS = auto()
    BACK = auto()

    @classproperty
    def prompt(self) -> str:
        return ":"


class AdvancedSettingsMenu(MenuTemplate):
    DISPLAY = auto()
    SELECTION = auto()
    SAMPLING = auto()
    PLAYBACK_BAR = auto()
    EVALUATION = auto()
    BACK = auto()

    @classproperty
    def prompt(self) -> str:
        return ":"


class ReadmeMenu(MenuTemplate):
    RULES = auto()
    SETTINGS = auto()
    ADVANCED_SETTINGS = auto()
    AUTHORS = auto()
    BACK = auto()

    @classproperty
    def prompt(self) -> str:
        return "Enter the number of INFO you want to get:"


class QuestionMenu(MenuTemplate):
    PLAY_SAMPLE = auto()
    GET_A_CLUE = auto()
    GIVE_ANSWER = auto()

    @classproperty
    def prompt(self) -> str:
        return ":"


class AnswerMenu(MenuTemplate):
    @classproperty
    def prompt(self) -> str:
        return ""


class EvaluationMenu(MenuTemplate):
    LISTEN_TO_EXTENDED_SAMPLE = auto()
    LISTEN_TO_ENTIRE_SONG = auto()
    EVALUATE_AS_CORRECT_ANSWER = auto()
    EVALUATE_AS_HALF_CORRECT_ANSWER = auto()
    EVALUATE_AS_WRONG_ANSWER = auto()
    EVALUATE_AS_NO_ANSWER = auto()

    @classproperty
    def prompt(self) -> str:
        return ":"


class AwaitMenu(MenuTemplate):
    @classproperty
    def prompt(self) -> str:
        return "Press ENTER to proceed further"
