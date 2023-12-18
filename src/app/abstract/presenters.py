from typing import Protocol

from pydantic import BaseModel

from app.abstract.viewers import AbstractViewer





class MenuPresenter:
    """
    Abstract class that represents the logic of menu navigation.
    Basically it is constructed from a pydantic model, which gives data to represent,
    and a viewer, which displays this data as a menu.

    When run, it displays the menu, receives user input, validates it, and returns the result.

    Roughly implemented as Presenter component of the MVP pattern.
    """

    def _receive_input(self) -> None:
        while True:
            self._current_input = input()
            try:
                self._validator.validate(self._current_input)
            except InvalidInputError as exc:
                msg = f"{exc}. {bold('Try again.')}"
                self._viewer.display(msg)
            else:
                break

    def run(self) -> None:
        self._show_input_request()
        self._receive_input()
        self._process_input()
        self._mangle_input()
