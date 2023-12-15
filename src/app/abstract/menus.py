from typing import Protocol


class Menu(Protocol):
    """
    Class that represents menu.
    """

    def represent(self) -> str:
        ...

    def receive(self) -> str:
        ...

    def mangle(self, input_text: str) -> str:
        ...
