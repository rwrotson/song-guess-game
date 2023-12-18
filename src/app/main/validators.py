from typing import Any, Protocol

from pydantic import BaseModel, ValidationError

from app.exceptions import InvalidInputError
from app.main.presenters import Presenter


class Validator(Protocol):
    """
    Class that validates user input.
    """

    def validate(self) -> None:
        ...


class ChoiceInputValidator(Validator):
    def __init__(self, *, presenter: "Presenter"):
        self._max_number = presenter.menu.options_number


class ChoiceInputValidator2:
    def __init__(self, *, max_number: int) -> None:
        self._max_number = max_number

    def validate(self, input_text: str, /) -> None:
        try:
            input_number = int(input_text)
        except ValueError:
            raise InvalidInputError("You must enter a number.")
        else:
            if input_number not in range(1, self._max_number + 1):
                raise InvalidInputError(f"You can only enter a number between 1 and {self._max_number}.")


class TextInputValidator2:
    def __init__(self, *, model: BaseModel, field_name: str) -> None:
        # идея 1: передавать в ините цельный филд
        # идея 2: перенести логику валидации отдельного поля из модели сюда
        self._model = model
        self._field_name = field_name

    def _validate_field(self, value: str, /):
        self._model.__pydantic_validator__.validate_assignment(
            self._model.model_construct(),
            field_name=self._field_name,
            field_value=value,
        )

    def validate(self, input_text: str, /) -> None:
        try:
            self._validate_field(input_text)
        except ValidationError as exc:
            raise InvalidInputError(exc.errors()[0]["msg"])


def validator_factory(presenter: Presenter) -> Validator:
    if presenter.menu.menu_type == MenuType.CHOICE:
        return ChoiceInputValidator(presenter=presenter)
    elif presenter.menu.menu_type == MenuType.TEXT:
        return TextInputValidator(presenter=presenter)
    else:
        raise ValueError(f"Unknown menu type: {presenter.menu.menu_type}.")