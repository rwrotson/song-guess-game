import os
import subprocess
from enum import StrEnum
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Self

from magic import from_file as get_file_format
from pydub import AudioSegment, effects
from pydub.utils import get_player_name

from app.exceptions import NotSupportedFormatError


class AllowedFormats(StrEnum):
    FLAC = "audio/x-flac"
    MP3 = "audio/mpeg"
    WAV = "audio/x-wav"

    @classmethod
    def from_path(cls, path: str | Path) -> Self:
        if isinstance(path, Path):
            path = str(path)
        file_format = get_file_format(path, mime=True)
        try:
            return cls(file_format)
        except ValueError:
            raise NotSupportedFormatError("Not correct format of file")


class PlayableSegment(AudioSegment):
    @staticmethod
    def _play_with_ffplay(audiosegment: AudioSegment) -> None:
        player = get_player_name()
        with NamedTemporaryFile("w+b", suffix=".wav") as f:
            audiosegment.export(f.name, "wav")
            default_command = [player, "-nodisp", "-autoexit", "-hide_banner"]
            log_suppress_param = ["-loglevel", "quiet"]

            subprocess.call(default_command + log_suppress_param + [f.name])

    def play(self, start: int = 0) -> None:
        audio = effects.normalize(self[start:])
        self._play_with_ffplay(audio)

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


def sigterm_handler(signum, frame):
    from multiprocessing import active_children

    for child_process in active_children():
        child_process.terminate()
    exit(0)


def player_worker(audio: PlayableSegment, start: int = 0) -> None:
    import signal

    signal.signal(signal.SIGTERM, sigterm_handler)

    sample = audio[start:]
    normalized_sample = effects.normalize(sample)
    normalized_sample.play()


def get_audiofiles_paths(path: str | Path) -> set[str]:
    all_files = set()
    for path, _, files in os.walk(path):
        for file in files:
            all_files.add(os.path.join(path, file))
    return {f for f in all_files if get_file_format(f, mime=True) in AllowedFormats}
