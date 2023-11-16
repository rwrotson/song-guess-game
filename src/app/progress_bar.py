import time
from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property

from app.formatters import blue, magenta, red
from app.settings.models import PlaybackBarSettings

import cursor


class Clock:
    """
    Class for timing the playback.
    """
    __slots__ = ["_start_time", "_current_time"]

    def __init__(self):
        self._start_time = None
        self._current_time = None

    def start(self):
        self._start_time = datetime.now()

    @property
    def time_passed(self) -> int:
        if self._start_time is None:
            raise ValueError("Clock is not started.")

        timedelta = datetime.now() - self._start_time
        return timedelta.seconds * 1000 + timedelta.microseconds // 1000


class TimeDisplay:
    """
    Class that displays time of the song.
    """
    __slots__ = ["_song_length", "_current_time"]

    def __init__(self, song_length: int, current_time: int):
        self._song_length = song_length // 1000
        self._current_time = current_time // 1000

    @property
    def _minutes_passed(self) -> str:
        return f"{self._current_time // 60 % 60:02d}:{self._current_time % 60:02d}"

    @property
    def _minutes_elapsed(self) -> str:
        seconds_elapsed = self._song_length - self._current_time
        return f"{seconds_elapsed // 60 % 60:02d}:{seconds_elapsed % 60:02d}"

    def show(self) -> str:
        return f"{self._minutes_passed}/{self._minutes_elapsed}"

    def update_current_time(self, current_time: int) -> None:
        self._current_time = current_time // 1000


@dataclass(frozen=True, slots=True)
class PlaybackParams:
    """
    Times in ms.
    """
    song_length: int
    start_time: int
    question_mark: int
    clue_marks: list[int] = field(default_factory=list)


class BarDisplay:
    """
    Progress bar for playback.

    Time in ms.
    """
    def __init__(self, song_length: int, question_mark: int, clue_marks: list[int], start_time: int, config: PlaybackBarSettings):
        self._bar_length = config.bar_length
        self._empty_char = config.empty_char
        self._full_char = config.full_char

        bar_length_in_ms = song_length // config.bar_length
        self._start_bar_n = start_time // bar_length_in_ms + 1
        self._qmark_bar_n = question_mark // bar_length_in_ms + 1 if config.enable_question_mark else None
        self._cmark_bar_ns = [mark // bar_length_in_ms + 1 for mark in clue_marks] if config.enable_clue_marks else []

        self._n = 0
        self._prev_bar = None
        self._bar = ""

    @cached_property
    def _empty_bar(self) -> str:
        return self._empty_char * self._bar_length

    def update_bar(self) -> None:
        self._n += 1
        self._prev_bar = self._bar
        if self._n == self._qmark_bar_n and self._n in self._cmark_bar_ns:
            self._bar += magenta(self._full_char)
        elif self._n == self._qmark_bar_n:
            self._bar += red(self._full_char)
        elif self._n in self._cmark_bar_ns:
            self._bar += blue(self._full_char)
        else:
            self._bar += self._full_char

    @property
    def current_bar(self) -> str:
        return self._bar + self._empty_bar[self._n:]
    r
    @property
    def previous_bar(self) -> str:
        return self._prev_bar + self._empty_bar[self._n + 1:]


class Playback:
    """
    Progress bar for playback.
    Time in ms.
    """
    def __init__(self, params: PlaybackParams, config: PlaybackBarSettings):
        self._song_length = params.song_length
        self._start_time = params.start_time

        self._config = config
        self._start_time = params.start_time
        bar_length_in_ms = params.song_length // config.bar_length

        self._bar = BarDisplay(
            song_length=params.song_length,
            question_mark=params.question_mark,
            clue_marks=params.clue_marks,
            start_time=params.start_time,
            config=config,
        )
        self._time = TimeDisplay(
            song_length=params.song_length,
            current_time=params.start_time,
        )
        self._clock = Clock()

    def start(self) -> None:
        self._clock.start()

        current_time = self._clock.time_passed + self._start_time
        self._time.update_current_time(current_time=current_time)

        while current_time < self._song_length:
            with cursor.HiddenCursor():
                self._time.update_current_time(current_time)

                print(current_time)
                self._time.update_current_time(current_time)
                print(self._time.show())
                print(self._bar.show_for_step_n(self._clock.current_bar_n))

                current_time = self._clock.time_passed + self._start_time
                time.sleep(self._config.update_frequency)

    def display(self) -> str:
        initial_space = self._config.space_char * 10

        yield (
            f"{initial_space}"
            f"{self._bar.show_for_step_n(self._clock.current_bar_n)} | "
            f"{self._time.show()}\r"
        )
        yield (
            f"{initial_space}"
            f"{self._bar.show_for_step_n(self._clock.current_bar_n - 1)} | "
            f"{self._time.show()}\r"
        )


pl = Playback(
    params=PlaybackParams(
        song_length=100000,
        question_mark=20100,
        clue_marks=[20000, 40000, 60000, 80000],
        start_time=0,
    ),
    config=PlaybackBarSettings(),
)
for _ in range(60):
    with cursor.HiddenCursor():
        print(pl._bar.show(), end="\r")
        pl._bar.update_bar()
        time.sleep(0.2)

print(" " * 100, end="\r")
