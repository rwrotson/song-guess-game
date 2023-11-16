from dataclasses import dataclass
from typing import Protocol

from app.formatters import colored_fore, imitate_typing, ForeColor, bold


class Viewer(Protocol):
    def display(self, text: str) -> None:
        ...


class TypingDisabledViewer:
    def display(self, text: str) -> None:
        print(text)


@dataclass(slots=True)
class TypingEnabledView:
    min_delay: float
    max_delay: float

    def display(self, text: str) -> None:
        imitate_typing(
            text=text,
            min_delay=self.min_delay,
            max_delay=self.max_delay,
        )
