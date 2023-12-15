from abc import ABC, abstractmethod
from enum import auto
from functools import cache

from app.utils import EnumeratedStrEnum, split_camel_case_string, classproperty


class MenuInfo(EnumeratedStrEnum, ABC):
    @classproperty
    @abstractmethod
    def prompt(self) -> str:
        pass
    
    @classmethod
    @classproperty
    @cache
    def name(cls) -> str:
        words = split_camel_case_string(cls.__name__)
        if words[-1] == "Menu" and len(words) > 1:
            words.pop()
        return " ".join(words)


class MainMenu(MenuInfo):
    PLAY = auto()
    SETTINGS = auto()
    README = auto()
    EXIT = auto()

    @classproperty
    def prompt(self) -> str:
        return "Select main menu section:"


class SettingsMenu(MenuInfo):
    MAIN_SETTINGS = auto()
    ADVANCED_SETTINGS = auto()
    SHOW_CURRENT_SETTINGS = auto()
    EDIT_CONFIG_FILE = auto()
    BACK = auto()

    @classproperty
    def prompt(self) -> str:
        return "Select settings menu section:"


class MainSettingsMenu(MenuInfo):
    GAME_SETTINGS = auto()
    PLAYER_SETTINGS = auto()
    BACK = auto()

    @classproperty
    def prompt(self) -> str:
        return ":"


class AdvancedSettingsMenu(MenuInfo):
    DISPLAY = auto()
    SELECTION = auto()
    SAMPLING = auto()
    PLAYBACK_BAR = auto()
    EVALUATION = auto()
    BACK = auto()

    @classproperty
    def prompt(self) -> str:
        return ":"


class ReadmeMenu(MenuInfo):
    RULES = auto()
    SETTINGS = auto()
    ADVANCED_SETTINGS = auto()
    AUTHORS = auto()
    BACK = auto()

    @classproperty
    def prompt(self) -> str:
        return "Enter the number of INFO you want to get:"


class QuestionMenu(MenuInfo):
    PLAY_SAMPLE = auto()
    GET_A_CLUE = auto()
    GIVE_ANSWER = auto()

    @classproperty
    def prompt(self) -> str:
        return ":"
    
    
class AnswerMenu(MenuInfo):
    @classproperty
    def prompt(self) -> str:
        return ""


class EvaluationMenu(MenuInfo):
    LISTEN_TO_EXTENDED_SAMPLE = auto()
    LISTEN_TO_ENTIRE_SONG = auto()
    EVALUATE_AS_CORRECT_ANSWER = auto()
    EVALUATE_AS_HALF_CORRECT_ANSWER = auto()
    EVALUATE_AS_WRONG_ANSWER = auto()
    EVALUATE_AS_NO_ANSWER = auto()

    @classproperty
    def prompt(self) -> str:
        return ":"


class AwaitMenu(MenuInfo):
    @classproperty
    def prompt(self) -> str:
        return "Press ENTER to proceed further"
