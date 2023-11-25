import os
import subprocess
import yaml
from typing import Any, Self, TypeAlias

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

from app.consts import CONFIG_FILE_PATH
from app.models import BaseModel


class GameSettings(BaseModel):
    """
    Main settings section.
    """

    sample_duration: float = Field(
        gt=0.05,
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


class PlayerSettings(BaseModel):
    """
    Settings of a player: name and path to her music.
    """

    name: str = Field(
        min_length=1,
        max_length=20,
        default="",
        description="Enter the name of the player.",
    )
    path: str = Field(
        default="",
        description="Enter the path to the folder with player's audiofiles.",
    )

    @classmethod
    @field_validator('path')
    def check_if_path_exists(cls, path: str):
        assert os.path.exists(path), 'Sorry, there is no such folder.'
        return path

    @classmethod
    @field_validator('players_folders')
    def check_if_there_are_audiofiles(cls, path):
        assert len(get_all_audiofiles(path)) != 0, 'Sorry, there are no supported audiofiles in this folder.'
        return path


class DisplaySettings(BaseModel):
    """
    Settings of how the game is displayed.
    """

    color: bool = Field(
        default=True,
        description="Is coloring in the game interface enabled.",
    )


class SelectionSettings(BaseModel):
    """
    Settings of a selection of a songs in players' paths.
    """

    strategy: str = Field(
        pattern="naive|normalized",
        default="naive",
        description="Enter the strategy of choosing the next song from [naive|normalized].",
    )


class SamplingSettings(BaseModel):
    """
    Settings of how the samples inside songs are chosen.
    """

    from_: float = Field(
        ge=0,
        default=2.0,
        description="Enter number of seconds from the start of the song from which the sampling is possible.",
    )
    to_finish: float = Field(
        ge=0,
        default=3,
        description="Enter number of seconds till the finish of the song from which the sampling is possible.",
    )
    strategy: str = Field(
        pattern="naive|normalized",
        default="normalized",
        description="Enter the strategy of choosing samples from seconds from [naive|normalized].",
    )


class TypingSettings(BaseModel):
    """
    Settings of how the text is typed on display.
    """

    enabled: bool = Field(
        default=True,
        description="Is typing of the text enabled, or it is displayed instantly.",
    )
    min_delay: float = Field(
        gt=0.0,
        default=0.01,
        description="Enter minimal number of seconds between two characters.",
    )
    max_delay: float = Field(
        gt=0.0,
        default=0.1,
        description="Enter maximum number of seconds between two characters.",
    )


class PlaybackBarSettings(BaseModel):
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


class EvaluationSettings(BaseModel):
    """
    Settings of how the answers are evaluated.
    """

    full_answer: int | float = Field(
        ge=0,
        default=1.0,
        description="Enter the number of points for full answer.",
    )
    half_answer: int | float = Field(
        ge=0,
        default=0.5,
        description="Enter the number of points for half answer.",
    )
    no_answer: int | float = Field(
        ge=0,
        default=0.0,
        description="Enter the number of points for no answer.",
    )
    wrong_answer: int | float = Field(
        le=0.0,
        default=0.0,
        description="Enter the negative number of points for wrong answer.",
    )
    clue_discont: float = Field(
        ge=0.0,
        le=1.0,
        default=0.1,
        description="Enter the discount in [0; 1] for each used clue.",
    )


YamlDict: TypeAlias = dict[str, dict[str, Any] | list[dict[str, str]]]


class Settings(BaseSettings):
    """
    All game settings.
    Can be initialized from default or from file, can be saved to yaml file.
    """

    game: GameSettings = Field(default=GameSettings())
    players: list[PlayerSettings] = Field(default_factory=lambda: [PlayerSettings()])
    typing: TypingSettings = Field(default=TypingSettings())
    selection: SelectionSettings = Field(default=SelectionSettings())
    sampling: SamplingSettings = Field(default=SamplingSettings())
    evaluation: EvaluationSettings = Field(default=EvaluationSettings())

    @staticmethod
    def _dict_from_yaml_file() -> YamlDict:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    @classmethod
    def load_from_file(cls) -> Self:
        return cls(**cls._dict_from_yaml_file())

    def update_from_file(self) -> None:
        yaml_dict = self._dict_from_yaml_file()

        fields = self.model_dump(exclude={"players"})

        for section_name in fields:
            setattr(self, section_name, self.__annotations__[section_name](**yaml_dict[section_name]))

        self.players = [PlayerSettings(**player) for player in yaml_dict["players"]]

    def save_to_file(self) -> None:
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as file:
            yaml.dump(self.model_dump(), file, allow_unicode=True)

    def set_to_default(self) -> None:
        fields = self.model_dump(exclude={"players"})

        for section_name in fields:
            setattr(self, section_name, self.__annotations__[section_name]())

    @staticmethod
    def edit_config():
        editor = os.environ.get('EDITOR', 'vi')
        subprocess.call([editor, CONFIG_FILE_PATH])
