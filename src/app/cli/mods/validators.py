from dataclasses import dataclass
from functools import cache, cached_property
from typing import Any, Iterable, Protocol, Self

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

    def validate(self, input_text: str, /, *, step_number: int = 0) -> Any:
        ...


class NoValidator:
    """
    Class that validates user input.
    """

    __slots__ = ("_default_input",)

    def __init__(self, default_input: str = "none"):
        self._default_input = default_input

    @property
    def steps_number(self) -> int:
        return 1

    def validate(self, input_text: str, /, *, step_number: int = 0) -> str:
        return input_text if input_text else self._default_input


@dataclass(frozen=True)
class ChoicesSet:
    choices: set[str]

    @classmethod
    def from_iterable(cls, iterable: Iterable[str]) -> Self:
        return cls(set(map(str, iterable)))


class ChoicesSetValidator:
    """
    Class that validates user input.
    """

    __slots__ = ("_choices",)

    def __init__(self, *choices: ChoicesSet) -> None:
        self._choices = choices

    @property
    def steps_number(self):
        return len(self._choices)

    def validate(self, input_text: str, /, *, step_number: int = 0) -> str:
        choices_set = self._choices[step_number]
        if input_text not in choices_set:
            raise InvalidInputError(
                f"Enter one of the following: {', '.join(choices_set)}."
            )
        return input_text


class MaxNumberValidator:
    """
    Class that validates user input.
    """

    __slots__ = ("_max_ns",)

    def __init__(self, *max_numbers: int) -> None:
        self._max_ns = max_numbers

    @property
    def steps_number(self) -> int:
        return len(self._max_ns)

    def validate(self, input_text: str, /, *, step_number: int = 0) -> int:
        max_n = self._max_ns[step_number]

        try:
            input_number = int(input_text)

        except ValueError:
            raise InvalidInputError("You must enter a number.")

        else:
            if input_number not in range(1, max_n + 1):
                raise InvalidInputError(f"Enter a number between 1 and {max_n}.")
            return input_number


class CompositeValidator:
    """
    Class that validates user input.
    """

    __slots__ = ("_validators", "__dict__")

    def __init__(self, *validators: Validator) -> None:
        if any(v.steps_number != 1 for v in validators):
            raise ValueError("All validators must have exactly one step.")
        self._validators = validators

    @cached_property
    def steps_number(self) -> int:
        return len(self._validators)

    def validate(self, input_text: str, /, *, step_number: int) -> Any:
        return self._validators[step_number].validate(input_text)


class ModelValidator:
    """
    Class that validates user input.
    """

    __slots__ = ("_model", "_accept_null_for_defaults", "__dict__")

    def __init__(self, model: BaseModel, accept_null_for_defaults: bool = True) -> None:
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

    def validate(self, input_text: str, /, *, step_number: int) -> Any:
        default = self._get_default_value_by_step_number(step_number)
        if input_text == "" and self._accept_null_for_defaults and default is not None:
            return default

        try:
            field_name = self._field_name_by_step_number(step_number)
            partial_model = self._model.__pydantic_validator__.validate_assignment(
                self._model.model_construct(),
                field_name=field_name,
                field_value=input_text,
            )
            return getattr(partial_model, field_name)

        except ValidationError as exc:
            raise InvalidInputError(exc.errors()[0]["msg"])
