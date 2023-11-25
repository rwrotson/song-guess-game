from abc import ABC, abstractmethod

from pydantic import ValidationError

from app.abstract.models import BaseModel
from app.abstract.views import Viewer
from app.formatters import bold, separate_line


class Presenter(ABC):
    """
    Abstract class that represents the logic of menu navigation.
    Basically it is constructed from a pydantic model, which gives data to represent,
    and a viewer, which displays this data as a menu.

    When run, it displays the menu, receives user input, validates it, and returns the result.

    Roughly implemented as Presenter component of the MVP pattern.
    """

    def __init__(self, model: BaseModel, viewer: Viewer) -> None:
        self._model = model
        self._viewer = viewer

        self._current_input: str = ""

    def _display(self, text: str, is_separate_line: bool = True) -> None:
        if is_separate_line:
            text = separate_line(text)
        self._viewer.display(text=text)

    @abstractmethod
    def _show_input_request(self):
        ...

    def _receive_input(self) -> None:
        while True:
            self._current_input = input()
            try:
                self._validate_input()
            except ValidationError as exc:
                msg = f"{exc.errors()[0]['msg']}. {bold('Try again.')}"
                self._display(text=msg)
            else:
                break

    @abstractmethod
    def _validate_input(self):
        ...

    @abstractmethod
    def _mangle_input(self) -> None:
        ...

    @abstractmethod
    def _proceed_input(self) -> None:
        ...

    def run(self) -> None:
        self._show_input_request()

        self._receive_input()
        self._mangle_input()

        self._proceed_input()
