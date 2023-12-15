from typing import Protocol


class Viewer(Protocol):
    """
    Class that displays text to the user.
    """

    def display(self, text: str, /, *, is_bold: bool = False, is_sep_line: bool = True) -> None:
        ...
