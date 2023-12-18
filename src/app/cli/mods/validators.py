from abc import ABC, abstractmethod
from functools import cache, cached_property
from typing import Any, Iterable, Protocol

from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticUndefined

from app.cli.exceptions import InvalidInputError


class Validator(Protocol):
    """
    Class that validates user input.
    """
    @property
    def steps_number(self) -> int:
        ...

    def validate(self, text_input: str, /, **kwargs) -> None:
        ...


class OneStepValidator(ABC):
    """
    Validator independable of step number.
    """

    @property
    def steps_number(self) -> int:
        return 1

    def validate(self, text_input: str, /, **kwargs) -> None:
        ...


class MultiStepValidator(Protocol):
    """
    Validator dependent on step number.
    """

    @cached_property
    def steps_number(self) -> int:
        ...

    def validate(self, text_input: str, /, *, step_number: int) -> None:
        ...


class ChoiceValidator(OneStepValidator):
    """
    Class that validates user input.
    """
    def __init__(self, choices: Iterable[int, str]) -> None:
        self._choices: set[str] = set(map(str, choices))

    def validate(self, text_input: str, /, **kwargs) -> None:
        if text_input not in self._choices:
            raise InvalidInputError(f"Enter one of the following: {', '.join(self._choices)}.")


class MaxNumberValidator(OneStepValidator):
    """
    Class that validates user input.
    """
    def __init__(self, max_number: int) -> None:
        self._max_n = max_number

    def validate(self, text_input: str, /, **kwargs) -> None:
        try:
            input_number = int(text_input)
        except ValueError:
            raise InvalidInputError("You must enter a number.")
        else:
            if input_number not in range(1, self._max_n + 1):
                raise InvalidInputError(f"Enter a number between 1 and {self._max_n}.")


def _validate_pydantic_field(model: BaseModel, field_name: str, field_value: Any) -> None:
    model.__pydantic_validator__.validate_assignment(
        model.model_construct(),
        field_name=field_name,
        field_value=field_value,
    )


class FieldValidator:
    """
    Class that validates user input.
    """
    def __init__(self, model: BaseModel, field_name: str) -> None:
        self._model = model
        self._field_name = field_name

    def validate(self, text_input: str, /) -> None:
        try:
            _validate_pydantic_field(self._model, self._field_name, text_input)
        except ValidationError as exc:
            raise InvalidInputError(exc.errors()[0]["msg"])


class CompositeValidator:
    """
    Class that validates user input.
    """
    def __init__(self, *validators: OneStepValidator) -> None:
        self._validators = validators

    @cached_property
    def steps_number(self) -> int:
        return len(self._validators)

    def validate(self, text_input: str, /, *, step_number: int) -> None:
        self._validators[step_number].validate(text_input)


class ModelValidator:
    """
    Class that validates user input.
    """
    def __init__(self, model: BaseModel, *, accept_null_for_defaults: bool = True) -> None:
        self._model = model
        self._accept_null_for_defaults = accept_null_for_defaults

    @cached_property
    def steps_number(self) -> int:
        return len(self._model.model_fields)

    @cache
    def _field_name_by_step_number(self, step_number: int, /) -> str:
        return list(self._model.model_fields)[step_number]

    @cache
    def _get_default_value_by_step_number(self, step_number: int, /) -> Any | None:
        field_name = self._field_name_by_step_number(step_number)
        default = self._model.model_fields[field_name].default
        return None if default == PydanticUndefined else default

    def validate(self, text_input: str, /, *, step_number: int) -> None:
        default = self._get_default_value_by_step_number(step_number)
        if text_input == "" and self._accept_null_for_defaults and default:
            return

        try:
            field_name = self._field_name_by_step_number(step_number)
            _validate_pydantic_field(self._model, field_name, text_input)

        except ValidationError as exc:
            raise InvalidInputError(exc.errors()[0]["msg"])
