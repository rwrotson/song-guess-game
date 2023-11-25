from typing import Protocol

from app.formatters import colored_fore, imitate_typing, ForeColor


class Viewer(Protocol):
    """
    Class that displays text to the user.
    """

    def display(self, text: str) -> None:
        ...


class TypingDisabledViewer:
    __slots__ = ("color",)

    def __init__(self, color: ForeColor = ForeColor.WHITE) -> None:
        self.color = color

    def display(self, text: str) -> None:
        print(colored_fore(text=text, color=self.color), flush=True)


class TypingEnabledViewer:
    __slots__ = ("min_delay", "max_delay", "color")

    def __init__(self, min_delay: float, max_delay: float, color: ForeColor = ForeColor.WHITE) -> None:
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.color = color

    def display(self, text: str) -> None:
        imitate_typing(
            text=colored_fore(text=text, color=self.color),
            min_delay=self.min_delay,
            max_delay=self.max_delay,
        )
