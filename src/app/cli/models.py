from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Any, Self

from pydantic import BaseModel

from app.cli.exceptions import IncorrectMenuConfigurationError
from app.cli.formatters import Text
from app.cli.mods.manglers import Mangler
from app.cli.mods.processors import Processor, Input
from app.cli.mods.representers import Representer
from app.cli.mods.validators import Validator
from app.cli.formatters import TemplateString


class MenuStepType(StrEnum):
    OPTIONS = auto()
    TEXT_INPUT = auto()


@dataclass(slots=True, frozen=True)
class MenuStep:
    """
    Class representing a single step in a menu.
    """

    name: str | None = None
    prompt: Text | None = None
    default: Any = None
    options: list[Text] = field(default_factory=list)

    @property
    def step_type(self) -> MenuStepType:
        return MenuStepType.OPTIONS if self.options else MenuStepType.TEXT_INPUT

    @property
    def options_number(self) -> int:
        return len(self.options)

    @classmethod
    def from_model_field(cls, model: BaseModel, model_field: str) -> Self:
        return cls(
            name=model_field,
            prompt=model.model_fields[model_field].description,
            default=model.model_fields[model_field].default,
        )

    def __len__(self):
        return self.options_number

    def __str__(self):
        return f"<{self.name}: {[option for option in self.options]}>"


class MenuType(StrEnum):
    OPTIONS = auto()
    TEXT_INPUT = auto()
    MIXED = auto()

    @classmethod
    def from_step_types(cls, *step_types: MenuStepType) -> Self:
        step_types = set(step_types)
        match len(step_types):
            case 1:
                return cls(step_types.pop().name)
            case _:
                return cls.MIXED


class Menu:
    """

    """
    __slots__ = ("_name", "_steps", "_representer", "_validator", "_mangler", "_processor")

    def __init__(
        self,
        *steps: MenuStep,
        representer: Representer,
        validator: Validator,
        mangler: Mangler,
        processor: Processor,
        name: str | None = None,
    ):
        self._name = name
        self._steps = steps

        self._representer = representer
        self._validator = validator
        self._mangler = mangler
        self._processor = processor

        self._validate_coherance()

    def _validate_coherance(self):
        mods = self._representer, self._validator, self._mangler
        step_numbers = {getattr(obj, "steps_number") for obj in mods}
        step_numbers -= {1, self.steps_number}
        if len(step_numbers) != 0:
            raise IncorrectMenuConfigurationError(
                f"Some of the menu components have different number of steps "
                f"than 1 or than number of steps in menu model == {self.steps_number}."
            )

    @property
    def menu_type(self) -> MenuType:
        return MenuType.from_step_types(*self._steps)

    @property
    def steps_number(self) -> int:
        return len(self._steps)

    def represent(self, *, step_number: int) -> TemplateString:
        step_model = self._steps[step_number]
        return self._representer.represent(step_model, step_number=step_number)

    @staticmethod
    def receive(text: str = ""):
        return input(text).strip()

    def validate(self, input_text: str, *, step_number: int) -> Any:
        return self._validator.validate(input_text, step_number=step_number)

    def mangle(self, input_text: str, *, step_number: int, option_name: str = "") -> TemplateString:
        return self._mangler.mangle(
            input_text,
            option_name=option_name,
            step_number=step_number,
        )

    def process(self, raw: str, validated: Any, option_name: str | None, *, step_number: int) -> None:
        if option_name:
            option_name = option_name.upper()
        input_ = Input(raw=raw, validated=validated, option_name=option_name)
        return self._processor.process(input_, step_number=step_number)

    def __getitem__(self, item: int) -> MenuStep:
        return self._steps[item]

    def __str__(self):
        if self.steps_number == 1:
            return str(self._steps[0])
        return f"<{self._name or "Untitled menu"}: {self.steps_number} steps deep>"
