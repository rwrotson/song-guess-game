from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class Input:
    raw: str
    validated: Any
    option_name: str | None  # in upper case


class Processor(Protocol):
    """
    Class that processes user input and changes app state due to user's command.
    """

    def process(self, input_: Input, step_number: int = 0) -> None: ...
