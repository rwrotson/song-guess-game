from typing import Protocol


class InputProcessor(Protocol):
    """
    Class that processes user input and changes app state due to user's command.
    """
    def __init__(self, state: State):
        ...

    def process(self, input_text: str, /) -> None:
        ...
