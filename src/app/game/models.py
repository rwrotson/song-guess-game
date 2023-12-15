import os
import random
from dataclasses import dataclass, field
from enum import StrEnum, auto
from pathlib import Path
from typing import Generator, Self

import music_tag
from magic import from_file as get_file_format
from pydub import AudioSegment, effects
from pydub.playback import play

from app.exceptions import NotSupportedFormatError
from app.formatters import bold
from app.game.selection import RandomTimesStrategy


class AllowedFormats(StrEnum):
    FLAC = "audio/x-flac"
    MP3 = "audio/mpeg"
    WAV = "audio/x-wav"

    @classmethod
    def from_path(cls, path: Path) -> Self:
        file_format = get_file_format(path, mime=True)
        try:
            return cls(file_format)
        except ValueError:
            raise NotSupportedFormatError("Not correct format of file")


@dataclass(frozen=True, slots=True)
class Metadata:
    title: str
    artist: str
    album: str
    year: str
    length: int

    @classmethod
    def from_path(cls, path: Path) -> Self:
        data = music_tag.load_file(path)

        metadata = {}
        for field in cls.__annotations__.keys():
            try:
                metadata[field] = data[field].values[0]
            except (KeyError, IndexError):
                metadata[field] = None

        metadata["length"] = (int(data["#length"].values[0]) - 5) * 1000

        return cls(**metadata)

    def __str__(self):
        return bold(
            f"{self.artist} - {self.title}\n"
            f"({self.album}, {self.year})"
        )


class PlayableSegment(AudioSegment):
    def play(self, start: int = 0):
        play(self[start:])

    @classmethod
    def from_path(cls, path: Path) -> Self:
        format_ = AllowedFormats.from_path(path)

        match format_:
            case AllowedFormats.MP3:
                return PlayableSegment.from_mp3(file=path)
            case AllowedFormats.WAV:
                return PlayableSegment.from_wav(file=path)
            case AllowedFormats.FLAC:
                return PlayableSegment.from_file(file=path, format="flac")
            case _:
                raise NotSupportedFormatError("Not correct format of file")


class Sample:
    time: int
    sample: PlayableSegment
    times_played: int = 0

    def play(self):
        self.sample.play()


class HelpUsage:
    __slots__ = ("_max_repeats", "_max_clues", "_repeats_used", "_clues_used")

    def __init__(self, max_repeats: int, max_clues: int):
        self._max_repeats = max_repeats
        self._max_clues = max_clues

        self._repeats_used = 0
        self._clues_used = 0

    def use_repeat(self):
        if self._repeats_used + 1 <= self._max_repeats:
            self._repeats_used += 1

    def use_clue(self):
        if self._clues_used + 1 <= self._max_clues:
            self._clues_used += 1

    @property
    def max_repeats(self):
        return self._max_repeats

    @property
    def max_clues(self):
        return self._max_clues

    @property
    def repeats_used(self) -> int:
        return self._repeats_used

    @property
    def clues_used(self) -> int:
        return self._clues_used

    @property
    def repeats_left(self) -> int:
        return self._max_repeats - self._repeats_used

    @property
    def clues_left(self) -> int:
        return self._max_clues - self._clues_used

    def __str__(self):
        return f"<Repeats: {self.repeats_left}, clues: {self.clues_left}>"


class Evaluation(StrEnum):
    FULL_ANSWER = auto()
    HALF_ANSWER = auto()
    WRONG_ANSWER = auto()
    NO_ANSWER = auto()


@dataclass(slots=True)
class Answer:
    answer_prompt: str
    evaluation: Evaluation


@dataclass(slots=True)
class QuestionSong:
    audio: PlayableSegment
    metadata: Metadata
    question_sample: Sample
    clue_samples: list[Sample]

    help_usage: HelpUsage = field(default_factory=HelpUsage)
    answer: Answer | None = None

    @classmethod
    def from_path(cls, path: Path):
        audio = PlayableSegment.from_path(path)
        metadata = Metadata.from_path(path)
        all_samples = cls.get_samples()

    def _get_samples(self):
        length = self.metadata.length
        random_times_strategy: RandomTimesStrategy = ...
        sample_times = random_times_strategy()
        samples_list = []
        for start in list_of_start_times:
            sample = effects.normalize(self.audio)[start:start + length * 1000]
            samples_list.append(sample)
        return samples_list

    def _set_sample_time(self, ):
        pass

    def _set_clue_samples(self):
        pass


class Audiofile:
    path: Path
    filename: str
    format: AllowedFormats

    __slots__ = ["path", "filename", "format", "song_object"]

    def __init__(self, path: Path):
        self.format = AllowedFormats.from_path(path)
        self.path = path
        self.filename = path.name


class Player:
    id: int
    name: str
    library_path: Path
    audiofiles: set[Audiofile]
    songs: list[QuestionSong]
    help_usage: HelpUsage

    __slots__ = ("id", "name", "library_path", "color", "audiofiles", "songs", "help_usage")

    def __init__(self, *, id_: int, name: str, library_path: Path) -> None:
        self.id = id_
        self.name = name
        self.library_path = library_path

        self.audiofiles = self.get_all_audiofiles()
        self.songs = []
        self.help_usage = HelpUsage()

    def get_all_audiofiles(self) -> set[Audiofile]:
        all_files = set()
        for path, _, files in os.walk(self.library_path):
            for file in files:
                all_files.add(os.path.join(path, file))
        return {
            f for f in all_files
            if get_file_format(f, mime=True) in AllowedFormats
        }

    def _choose_n_audiofiles(self, quantity: int) -> list[Audiofile]:
        return random.sample(self.audiofiles, quantity)

    def _initialize_song(self, audiofile: Audiofile) -> QuestionSong:
        pass


class GameCounter:
    _current_player_id: int
    _current_round: int

    __slots__ = ("_current_player_id", "_current_round", "_players_counter", "_rounds_counter")

    def __init__(self, players: int, rounds: int):
        self._players_counter = self.players_counter_gen(players)
        self._rounds_counter = self.rounds_counter_gen(rounds)

        next(self)

    @property
    def current_player_id(self) -> int:
        return self._current_player_id

    @property
    def current_round(self) -> int:
        return self._current_round

    @staticmethod
    def players_counter_gen(players_number: int) -> Generator[int, None, None]:
        while True:
            for i in range(players_number):
                yield i

    @staticmethod
    def rounds_counter_gen(rounds_number: int) -> Generator[int, None, None]:
        for i in range(rounds_number):
            yield i + 1

    def __next__(self):
        self._current_player_id = next(self._players_counter)
        if self._current_player_id == 0:
            self._current_round = next(self._rounds_counter)
        return self

    def __str__(self):
        return f"Round {self.current_round}, Player {self.current_player_id}"


class Game:
    rounds: int
    players: list[Player]
    game_counter: GameCounter

    __slots__ = ("rounds", "players", "game_counter")

    def __init__(self, players: list[Player], rounds: int) -> None:
        self.reset_game(players, rounds)

    def reset_game(self, players: list[Player], rounds: int) -> None:
        self.rounds = rounds
        self.players = players
        self.game_counter = GameCounter(players=len(players), rounds=rounds)

    @classmethod
    def from_pickle(cls, path: Path) -> Self:
        pass

    def pickle(self, path: Path) -> None:
        pass


class History:
    def __init__(self, *, game: Game):
        self.answers = {}

    def score_for_player_id(self, player_id: int, /) -> list[float]:
        pass

    def score_for_round(self, round_number: int, /) -> list[float]:
        pass
