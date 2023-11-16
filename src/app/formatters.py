from enum import StrEnum, auto
from time import sleep
from random import randrange

from colorama import init, Fore, Style


init(autoreset=True)


def bold(text: str) -> str:
    return Style.BRIGHT + text + Style.RESET_ALL


class ForeColor(StrEnum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()


def colored_fore(text: str, color: ForeColor) -> str:
    color_mapping = {
        ForeColor.RED: Fore.RED,
        ForeColor.GREEN: Fore.GREEN,
        ForeColor.YELLOW: Fore.YELLOW,
        ForeColor.BLUE: Fore.BLUE,
        ForeColor.MAGENTA: Fore.MAGENTA,
        ForeColor.CYAN: Fore.CYAN,
        ForeColor.WHITE: Fore.WHITE,
    }

    return color_mapping[color] + text + Fore.RESET


def red(text: str) -> str:
    return colored_fore(text, ForeColor.RED)


def blue(text: str) -> str:
    return colored_fore(text, ForeColor.BLUE)


def magenta(text: str) -> str:
    return colored_fore(text, ForeColor.MAGENTA)


def separate_line(text: str) -> str:
    return "\n" + text + "\n"


def imitate_typing(text: str, min_delay: int | float, max_delay: int | float) -> None:
    if isinstance(min_delay, float):
        min_delay = int(min_delay * 1000)
    if isinstance(max_delay, float):
        max_delay = int(max_delay * 1000)

    for char in text:
        print(char, end='', flush=True)
        delay = randrange(min_delay, max_delay)
        sleep(delay)
