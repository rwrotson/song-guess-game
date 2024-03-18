from enum import auto
from typing import override, Self
from string import Template

from colorama import init, Fore, Style

from app.utils import EnumeratedStrEnum, get_singleton_instance


init(autoreset=True)


_STYLE_FORMATTERS = {
    "bold": Style.BRIGHT,
    "dim": Style.DIM,
    "normal": Style.NORMAL,
    "r_style": Style.RESET_ALL,
}

_COLOR_FORMATTERS = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    "true_white": "",
    "r_color": Fore.RESET,
}


FORMATTERS = {**_STYLE_FORMATTERS, **_COLOR_FORMATTERS}


class TemplateStringOld(str):
    @override
    def format(self, *args, **kwargs) -> str:
        for k, v in kwargs.items():
            if v is None:
                kwargs[k] = ""
        return super().format(*args, **FORMATTERS, **kwargs)


class TemplateString(Template):
    @staticmethod
    def _patch_custom_formatters(kwargs: dict) -> dict:
        for k, v in kwargs.items():
            if v is None:
                kwargs[k] = ""
        kwargs.update(FORMATTERS)
        return kwargs

    @override
    def substitute(self, /, **kwargs) -> Self:
        kwargs = self._patch_custom_formatters(kwargs)
        return super().substitute(kwargs)

    @override
    def safe_substitute(self, /, **kwargs) -> Self:
        kwargs = self._patch_custom_formatters(kwargs)
        return super().safe_substitute(kwargs)

    def __add__(self, other: str | Self):
        self.template += str(other)
        return self

    def __radd__(self, other: str | Self):
        self.template = str(other) + self.template
        return self

    def __iadd__(self, other: str | Self):
        self.template += str(other)
        return self


def bold(text: str, /) -> str:
    return Style.BRIGHT + text + Style.RESET_ALL


def separate_line(text: str, /) -> str:
    text += "\n"
    return text


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
