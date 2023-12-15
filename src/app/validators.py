from app.exceptions import InvalidInputError

from pydantic import ValidationError


class ChoiceInputValidator:
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


class TextInputValidator:
    # logic-level validation
    def __init__(self, *, model: SettingsSection, field_name: str) -> None:
        # идея 1: передавать в ините цельный филд

        # идея 2: перенести логику валидации отдельного поля из модели сюда
        self._model = model
        self._field_name = field_name

    def validate(self, input_text: str, /) -> None:
        try:
            self._model.set_field(field_name=self._field_name, value=input_text)
        except ValidationError as exc:
            raise InvalidInputError(exc.errors()[0]["msg"])
