from typing import Protocol

from app.abstract.presenters import Presenter


class PresenterValidator(Protocol):
    """
    Class that validates user input.
    """

    def validate(self, presenter: Presenter) -> None:
        ...
