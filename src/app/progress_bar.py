import time
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

from app.formatters import blue, magenta, red
from app.settings.models import PlaybackBarSettings

import cursor


class Clock:
    """
    Class for timing the playback. Works as a stopwatch.
    """

    __slots__ = ["_start_time", "_current_time"]

    def __init__(self) -> None:
        self._start_time = None
        self._current_time = None

    def start(self) -> None:
        self._start_time = datetime.now()

    @property
    def time_passed(self) -> int:
        if self._start_time is None:
            raise ValueError("Clock is not started.")

        timedelta = datetime.now() - self._start_time
        return timedelta.seconds * 1000 + timedelta.microseconds // 1000


class TimeDisplay:
    """
    Class for displaying time of the song in the following format: mm:ss/mm:ss.
    """

    __slots__ = ["_song_length", "_current_time"]

    def __init__(self, song_length: int, current_time: int) -> None:
        self._song_length = song_length // 1000
        self._current_time = current_time // 1000

    @property
    def _minutes_passed(self) -> str:
        return f"{self._current_time // 60 % 60:02d}:{self._current_time % 60:02d}"

    @property
    def _minutes_elapsed(self) -> str:
        seconds_elapsed = self._song_length - self._current_time
        return f"{seconds_elapsed // 60 % 60:02d}:{seconds_elapsed % 60:02d}"

    @property
    def now(self) -> str:
        return f"{self._minutes_passed}/{self._minutes_elapsed}"

    def update(self, current_time: int) -> None:
        self._current_time = current_time // 1000


@dataclass(frozen=True, slots=True)
class PlaybackParams:
    song_length: int
    start_time: int
    question_mark: int
    clue_marks: list[int]


class BarDisplay:
    """
    Class for displaying progress bar.

    Time in ms.
    """

    __slots__ = ["_config", "_qmark_bar_n", "_cmark_bar_ns", "current_bar_n", "_bar", "_prev_bar"]

    def __init__(self, params: PlaybackParams, config: PlaybackBarSettings) -> None:
        self._config = config

        bar_length_in_ms = params.song_length // config.bar_length
        self._qmark_bar_n = params.question_mark // bar_length_in_ms + 1 if config.enable_question_mark else None
        self._cmark_bar_ns = [m // bar_length_in_ms + 1 for m in params.clue_marks] if config.enable_clue_marks else []

        current_bar_n = params.start_time // bar_length_in_ms + 1
        self.current_bar_n = 1
        self._bar = ""
        self._prev_bar = ""
        for _ in range(current_bar_n):
            self.update()

    def _empty_bar(self, length: int) -> str:
        return self._config.empty_char * length

    def update(self) -> None:
        self.current_bar_n += 1
        self._prev_bar = self._bar

        if (self.current_bar_n == self._qmark_bar_n) and (self.current_bar_n in self._cmark_bar_ns):
            self._bar += magenta(self._config.full_char)
        elif self.current_bar_n == self._qmark_bar_n:
            self._bar += red(self._config.full_char)
        elif self.current_bar_n in self._cmark_bar_ns:
            self._bar += blue(self._config.full_char)
        else:
            self._bar += self._config.full_char

    @property
    def current_bar(self) -> str:
        empty_bar_length = self._config.bar_length - self.current_bar_n
        return self._bar + self._empty_bar(length=empty_bar_length)

    @property
    def previous_bar(self) -> str:
        empty_bar_length = self._config.bar_length - (self.current_bar_n - 1)
        return self._prev_bar + self._empty_bar(length=empty_bar_length)


class Playback:
    """
    Progress display for playback with bar and time displays.

    Time in ms.
    """

    __slots__ = [
        "_config", "_song_length", "_start_time", "_current_time", "_clock", "_bar", "_time", "_display_generator"
    ]

    def __init__(self, params: PlaybackParams, config: PlaybackBarSettings) -> None:
        self._config = config

        self._song_length = params.song_length
        self._start_time = params.start_time
        self._current_time = params.start_time

        self._clock = Clock()
        self._bar = BarDisplay(params=params, config=config)
        self._time = TimeDisplay(
            song_length=params.song_length,
            current_time=params.start_time,
        )

        self._display_generator = self._get_display_string_generator()

    def start(self) -> None:
        self._clock.start()

        while self._current_time < self._song_length:
            with cursor.HiddenCursor():
                self._update()
                self.show()

                time.sleep(self._config.update_frequency)

    def _update(self) -> None:
        self._current_time = self._start_time + self._clock.time_passed
        self._time.update(current_time=self._current_time)

        bar_length_in_ms = self._song_length // self._config.bar_length
        if self._bar.current_bar_n < self._current_time // bar_length_in_ms + 1:
            self._bar.update()

    def _get_display_string_generator(self) -> Iterator[str]:
        initial_space = self._config.space_char * 10

        while True:
            yield f"{initial_space}{self._bar.current_bar} | {self._time.now}"

            if self._config.enable_bar_winking:
                yield f"{initial_space}{self._bar.previous_bar} | {self._time.now}"

    def show(self) -> None:
        print(next(self._display_generator), end=" \r")
