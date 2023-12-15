import time
from enum import auto
from random import randrange
from typing import Protocol

from colorama import init, Fore, Style

from app.utils import EnumeratedStrEnum, get_singleton_instance


init(autoreset=True)


class Formatter(Protocol):
    ...


def bold(text: str, /) -> str:
    return Style.BRIGHT + text + Style.RESET_ALL


def separate_line(text: str, /) -> str:
    return text + "\n"


class ForeColor(EnumeratedStrEnum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()

    @staticmethod
    def get_next_color():
        generator = _get_color_generator()
        return next(generator)


class _ColorGenerator:
    def __init__(self) -> None:
        import random

        self.max_color_number = len(ForeColor)
        self._current_color_number = random.randint(1, self.max_color_number)

    def __next__(self) -> ForeColor:
        if self._current_color_number > self.max_color_number:
            self._current_color_number = 1

        color = ForeColor.get_enum_by_order_number(self._current_color_number)
        self._current_color_number += 1

        return color


def _get_color_generator() -> _ColorGenerator:
    return get_singleton_instance(_ColorGenerator)


def colored_fore(text: str, /, *, color: ForeColor) -> str:
    if color == ForeColor.WHITE:
        return text

    color_mapping = {
        ForeColor.RED: Fore.RED,
        ForeColor.GREEN: Fore.GREEN,
        ForeColor.YELLOW: Fore.YELLOW,
        ForeColor.BLUE: Fore.BLUE,
        ForeColor.MAGENTA: Fore.MAGENTA,
        ForeColor.CYAN: Fore.CYAN,
    }

    return color_mapping[color] + text + Fore.RESET


def red(text: str, /) -> str:
    return colored_fore(text, color=ForeColor.RED)


def green(text: str, /) -> str:
    return colored_fore(text, color=ForeColor.GREEN)


def blue(text: str, /) -> str:
    return colored_fore(text, color=ForeColor.BLUE)


def magenta(text: str, /) -> str:
    return colored_fore(text, color=ForeColor.MAGENTA)


def imitate_typing(text: str, /, *, min_delay: int | float, max_delay: int | float) -> None:
    if isinstance(min_delay, float):
        min_delay = int(min_delay * 1000)
    if isinstance(max_delay, float):
        max_delay = int(max_delay * 1000)
    for char in text:
        print(char, end="", flush=True)
        delay = randrange(min_delay, max_delay) / 1000
        time.sleep(delay)
