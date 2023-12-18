from typing import Protocol

from app.cli.menus import Menu
from app.main.viewers import Viewer
from app.main.validators import Validator
from app.main.processors import Processor
from state import State


class AbstractPresenter(Protocol):
    """
    Abstract class that represents the logic of menu navigation.
    Basically it is constructed from a pydantic model, which gives data to represent,
    and a viewer, which displays this data as a menu.

    When run, it displays the menu, receives user input, validates it, and returns the result.

    Roughly implemented as Presenter component of the MVP pattern.
    """

    def __init__(self, *, menu: Menu, validator: Validator, processor: Processor, viewer: Viewer) -> None:
        ...

    def prepare(self, response):
        ...

    def validate(self):
        ...

    def process(self):
        ...


class Presenter:
    def __init__(self, *, menu: Menu, viewer: Viewer, validator: Validator, processor: Processor) -> None:
        self.menu = menu
        self.viewer = viewer
        self.validator = validator
        self.processor = processor

        self._input_text: str | None = None

    def prepare(self):
        self.menu.represent()
        self.menu.receive()

    def validate(self):
        self.validator.validate(self._input_text)

    def process(self):
        self.processor.process(self._input_text)
        self.menu.mangle(self._input_text)



def presenter_factory(state: State) -> Presenter:
    viewer = state._viewers.default_viewer
    menu_info =
