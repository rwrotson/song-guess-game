from dataclasses import dataclass
from enum import StrEnum, auto
from functools import cached_property
from typing import Self

from pydantic import BaseModel

from app.cli.templates import MenuTemplate


class MenuStepType(StrEnum):
    OPTIONS = auto()
    TEXT_INPUT = auto()


@dataclass
class MenuStep:
    name: str
    prompt: str
    options: type[MenuTemplate] | None = None

    @cached_property
    def step_type(self) -> MenuStepType:
        return MenuStepType.OPTIONS if self.options else MenuStepType.TEXT_INPUT

    @cached_property
    def options_number(self) -> int:
        return len(self.options) if self.options else 0

    @classmethod
    def from_menu_template(cls, menu_template: type[MenuTemplate]) -> Self:
        return cls(
            name=menu_template.name,
            prompt=menu_template.prompt,
            options=menu_template if len(menu_template) else None,
        )

    @classmethod
    def from_model_field(cls, model: BaseModel, field: str) -> Self:
        # TODO: add support for fields with choices
        # TODO: add support for fields with default values
        return cls(
            name=field,
            prompt=model.model_fields[field].description,
        )

    def __str__(self):
        return f"<{self.name}: {[item.name for item in self.options.as_list]}>"
