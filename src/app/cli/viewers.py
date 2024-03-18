from typing import Protocol

from app.cli.formatters import TemplateString, Text
from app.cli.utils import imitate_typing


class Viewer(Protocol):
    """
    Class that displays text to the user.
    """

    def display(self, text: Text, *, formatters_dict: dict[str, str] = None) -> None:
        ...


class TypingDisabledViewer:
    def __init__(self, formatters_dict: dict[str, str] = None) -> None:
        self._formatters_dict = formatters_dict

    def display(self, text: Text, *, formatters_dict: dict[str, str] = None) -> None:
        formatters_dict = formatters_dict or {}
        if isinstance(text, TemplateString):
            text = text.substitute(**self._formatters_dict, **formatters_dict)

        print(text, end="", flush=True)

    def __str__(self):
        return f"{self.__class__.__name__}({self._formatters_dict=})"


class TypingEnabledViewer:
    __slots__ = ("min_delay", "max_delay", "_formatters_dict")

    def __init__(
        self,
        *,
        min_delay: float,
        max_delay: float,
        formatters_dict: dict[str, str] = None,
    ) -> None:
        self.min_delay = min_delay
        self.max_delay = max_delay
        self._formatters_dict = formatters_dict

    def display(self, text: Text, *, formatters_dict: dict[str, str] = None) -> None:
        formatters_dict = formatters_dict or {}
        if isinstance(text, TemplateString):
            text = text.safe_substitute(**self._formatters_dict, **formatters_dict)

        imitate_typing(
            text,
            min_delay=self.min_delay,
            max_delay=self.max_delay,
        )

    def __str__(self):
        return f"{self.__class__.__name__}({self.min_delay=}, {self.max_delay=}, {self._formatters_dict})"
