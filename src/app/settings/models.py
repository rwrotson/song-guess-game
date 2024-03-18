import os
import subprocess
import yaml
from typing import Self

from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings

from app.models import OrderedModel
from app.consts import CONFIG_FILE_PATH, HISTORY_FILE_PATH, PICKLE_FILE_PATH
from app.files import get_audiofiles_paths
from app.utils import get_singleton_instance


class SettingsSection(OrderedModel):
    """
    Base class for all settings sections.
    """

    @property
    def fields_number(self) -> int:
        return len(self.model_fields)


class GameSettings(SettingsSection):
    """
    Main game settings section defining specifications of rules.
    """

    players_number: int = Field(
        ge=1,
        default=2,
        description="Enter the number of players in the game.",
    )
    sample_duration: float = Field(
        gt=0.1,
        default=1.0,
        description="Enter the duration of the sample in seconds.",
    )
    infinite_repeats: bool = Field(
        default=False,
        description="Is infinite repeats of the original sample allowed.",
    )
    repeats_number: int = Field(
        ge=1,
        default=5,
        description="Enter the number of repeats of the original sample.",
    )
    clues_number: int = Field(
        ge=0,
        default=10,
        description="Enter the number of clues for all game.",
    )
    clues_strategy: str = Field(
        pattern="random_next|new_next",
        default="new_next",
        description="Enter the strategy of choosing the next clue from [random_next|new_next].",
    )
    rounds_number: int = Field(
        ge=1,
        default=10,
        description="Enter the number of rounds in the game.",
    )


class PlayerSettings(SettingsSection):
    """
    Settings of a player: name and path to her music.
    """

    name: str = Field(
        min_length=1,
        max_length=20,
        default="default",
        description="Enter the name of the player.",
    )
    path: str = Field(
        default="",
        description="Enter the path to the folder with player's audiofiles.",
    )

    @field_validator("path")
    @classmethod
    def check_if_path_exists(cls, path: str) -> str:
        if not path:
            return path

        if not os.path.exists(path):
            raise ValueError("Sorry, there is no such folder.")
        return path

    @field_validator("path")
    @classmethod
    def check_if_there_are_audiofiles(cls, path: str) -> str:
        if not path:
            return path

        if len(get_audiofiles_paths(path)) == 0:
            raise ValueError("Sorry, there are no supported audiofiles in this folder.")
        return path


class DisplaySettings(SettingsSection):
    """
    Settings of how the game is displayed.
    """

    color_enabled: bool = Field(
        default=True,
        description="Is coloring in the game interface enabled.",
    )
    typing_enabled: bool = Field(
        default=True,
        description="Is typing of the text enabled, or it is displayed instantly.",
    )
    min_delay: float = Field(
        gt=0.0,
        lt=0.5,
        default=0.001,
        description="Enter minimal number of seconds between two characters.",
    )
    max_delay: float = Field(
        gt=0.0,
        lt=0.5,
        default=0.05,
        description="Enter maximum number of seconds between two characters.",
    )


class SelectionSettings(SettingsSection):
    """
    Settings of a selection of a songs in players' paths.
    """

    strategy: str = Field(
        pattern="naive|normalized_by_folder|normalized_by_album",
        default="naive",
        description="Enter the strategy of choosing the next song from [naive|normalized].",
    )


class SamplingSettings(SettingsSection):
    """
    Settings of how the samples inside songs are chosen.
    """

    from_: float = Field(
        ge=0,
        le=30,
        default=2.0,
        description="Enter number of seconds from the start of the song from which the sampling is possible.",
    )
    to_finish: float = Field(
        ge=0,
        le=30,
        default=3.0,
        description="Enter number of seconds till the finish of the song from which the sampling is possible.",
    )
    distance: float = Field(
        ge=1,
        default=5.0,
        description="Enter minimal distance between two samples on the same track in seconds.",
    )
    clues_quantity: int = Field(
        ge=1,
        le=10,
        default=3,
        description="Enter the number of clue samples for each song.",
    )
    strategy: str = Field(
        pattern="naive|normalized",
        default="normalized",
        description="Enter the strategy of choosing samples from seconds from [naive|normalized].",
    )


class PlaybackBarSettings(SettingsSection):
    """
    Settings of how the playback bar is displayed.
    """

    empty_char: str = Field(
        default="░",
        max_length=1,
        description="Enter the character used for empty part of the bar.",
    )
    full_char: str = Field(
        default="█",
        max_length=1,
        description="Enter the character used for full part of the bar.",
    )
    space_char: str = Field(
        default=" ",
        max_length=1,
        description="Enter the character used for space between parts of the bar.",
    )
    bar_length: int = Field(
        ge=20,
        le=100,
        default=50,
        description="Enter the length of the bar in characters.",
    )
    update_frequency: float = Field(
        ge=0.5,
        le=1.0,
        default=0.5,
        description="Enter the frequency of updating the bar in seconds.",
    )
    enable_flashing: bool = Field(
        default=False,
        description="Is playback bar flashing enabled.",
    )
    enable_question_mark: bool = Field(
        default=True,
        description="Is question mark displayed on the bar.",
    )
    enable_clue_marks: bool = Field(
        default=True,
        description="Are used clue marks displayed on the bar.",
    )


class EvaluationSettings(SettingsSection):
    """
    Settings of how the answers are evaluated.
    """

    full_answer: float = Field(
        ge=0,
        default=1.0,
        description="Enter the number of points for full answer.",
    )
    half_answer: float = Field(
        ge=0,
        default=0.5,
        description="Enter the number of points for half answer.",
    )
    no_answer: float = Field(
        ge=0,
        default=0.0,
        description="Enter the number of points for no answer.",
    )
    wrong_answer: float = Field(
        le=0.0,
        default=0.0,
        description="Enter the negative number of points for wrong answer.",
    )
    clue_discount: float = Field(
        ge=0.0,
        le=1.0,
        default=0.1,
        description="Enter the discount in [0; 1] for each used clue.",
    )


class ServicePathsSettings(SettingsSection):
    """
    Settings of where to store service files.
    """

    config_path: str = Field(
        default=str(CONFIG_FILE_PATH),
        description="Enter the path to the config file.",
    )
    game_pickle_path: str = Field(
        default=str(PICKLE_FILE_PATH),
        description="Enter the path to the game pickle file.",
    )
    history_log_path: str = Field(
        default=str(HISTORY_FILE_PATH),
        description="Enter the path to the history file.",
    )


class Settings(BaseSettings):
    """
    All game settings.
    Can be initialized from default or from file, can be saved to yaml file.
    """

    game: GameSettings = Field(default=GameSettings())
    players: list[PlayerSettings] = Field(default_factory=lambda: [PlayerSettings()])

    display: DisplaySettings = Field(default=DisplaySettings())
    selection: SelectionSettings = Field(default=SelectionSettings())
    sampling: SamplingSettings = Field(default=SamplingSettings())
    playback_bar: PlaybackBarSettings = Field(default=PlaybackBarSettings())
    evaluation: EvaluationSettings = Field(default=EvaluationSettings())
    service_paths: ServicePathsSettings = Field(default=ServicePathsSettings())

    @classmethod
    def load_from_file(cls) -> Self:
        yaml_dict = cls.config_file_as_dict()

        settings = cls(**yaml_dict)

        players_number = yaml_dict.get("game", {}).get("players_number", None)
        settings.players = [PlayerSettings(**p) for p in yaml_dict.get("players", [])]
        if players_number and (diff := players_number - len(settings.players)) > 0:
            settings.players.extend([PlayerSettings() for _ in range(diff)])
        if players_number and (players_number - len(settings.players) < 0):
            settings.players = settings.players[:players_number]

        settings.save_to_file()

        cls._instance = settings

        return settings

    def update_from_file(self) -> None:
        yaml_dict = self.config_file_as_dict()

        fields = self.model_dump(exclude={"players"})

        for section_name in fields:
            setattr(
                self,
                section_name,
                self.__annotations__[section_name](**yaml_dict[section_name]),
            )

        self.players = [PlayerSettings(**p) for p in yaml_dict.get("players", [])]
        players_number = yaml_dict.get("game", {}).get("players_number", None)
        if (diff := players_number - len(self.players)) > 0 and players_number:
            self.players.extend([PlayerSettings() for _ in range(diff)])

        self.save_to_file()

    def save_to_file(self) -> None:
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as file:
            yaml.dump(self.model_dump(), file, allow_unicode=True, sort_keys=False)

    def set_to_default(self) -> None:
        for section_name in self.model_dump(exclude={"players"}):
            setattr(self, section_name, self.__annotations__[section_name]())

        self.game.players_number = len(self.players)

        self.save_to_file()

    @staticmethod
    def config_file_as_dict() -> dict:
        with open(CONFIG_FILE_PATH, "r") as file:
            return yaml.safe_load(file) or {}

    @staticmethod
    def config_file_as_str() -> str:
        with open(CONFIG_FILE_PATH, "r") as file:
            return file.read()

    def edit_config_file(self) -> None:
        editor = os.environ.get("EDITOR", "nano")

        subprocess.call([editor, CONFIG_FILE_PATH])

        try:
            self.update_from_file()
        except ValidationError as e:
            self.save_to_file()
            raise e

    def __str__(self):
        import json

        return json.dumps(self.model_dump(), indent=4, ensure_ascii=False)


def get_settings() -> Settings:
    return get_singleton_instance(Settings)
