from typing import Any, Protocol

from pydantic import ValidationError

from app.abstract.models import BaseModel


class InputValidator(Protocol):
    """
    Class that validates user input.
    """

    def validate(self, input_text: Any) -> None:
        ...


class ChoiceInputValidator:
    def __init__(self, max_number: int) -> None:
        self._max_number = max_number

    def validate(self, input_text: str) -> None:
        try:
            input_number = int(input_text)
        except ValueError:
            raise ValidationError("You must enter a number.")
        else:
            if input_number not in range(1, self._max_number + 1):
                raise ValidationError(f"You can only enter a number between 1 and {self._max_number}.")


class TextInputValidator:
    def __init__(self, model: BaseModel, field_name: str) -> None:
        self._model = model
        self._field_name = field_name

    def validate(self, input_text: str) -> None:
        self._model.validate_field(field_name=self._field_name, value=input_text)
