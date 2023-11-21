import os
import random
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Self

import music_tag
from magic import from_file as get_file_format
from pydub import AudioSegment, effects
from pydub.playback import play

from app.exceptions import NotSupportedFormatError
from app.formatters import bold
from app.game.utils import RandomTimesStrategy


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


@dataclass(frozen=True, slots=True)
class QuestionSong:
    audio: PlayableSegment
    metadata: Metadata
    question_sample: Sample
    clue_samples: list[Sample]
    evaluation: float = 0.0

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


@dataclass(frozen=True, slots=True)
class Score:
    pass


class Player:
    id: int
    name: str
    library_path: Path
    audiofiles: set[Audiofile]
    songs: list[QuestionSong]

    __slots__ = ["id", "name", "library_path", "audiofiles"]

    def __init__(self, id_: int, name: str, library_path: Path) -> None:
        self.id = id_
        self.name = name
        self.library_path = library_path
        self.audiofiles = self.get_all_audiofiles()

    def get_all_audiofiles(self) -> set[Audiofile]:
        all_files = set()
        for path, _, files in os.walk(self.library_path):
            for file in files:
                all_files.add(os.path.join(path, file))
        return {
            f for f in all_files
            if get_file_format(f, mime=True) in AllowedFormats
        }

    def _choose_audiofiles(self, quantity: int) -> list[Audiofile]:
        return random.sample(self.audiofiles, quantity)

    def _initialize_song(self, audiofile: Audiofile) -> QuestionSong:
        pass

