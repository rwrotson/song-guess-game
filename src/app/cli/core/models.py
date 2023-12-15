from enum import StrEnum, auto
from functools import cached_property
from typing import Self

from pydantic import BaseModel

from app.cli.core.structs import MenuInfo


class MenuStepType(StrEnum):
    OPTIONS = auto()
    TEXT_INPUT = auto()


class MenuStep(BaseModel):
    # TODO: change to dataclass for performance
    name: str
    prompt: str
    options: type[MenuInfo] | None = None

    @cached_property
    def step_type(self) -> MenuStepType:
        return MenuStepType.OPTIONS if self.options else MenuStepType.TEXT_INPUT

    @classmethod
    def from_menu_info(cls, menu_info: type[MenuInfo]) -> Self:
        return cls(
            name=menu_info.name,
            prompt=menu_info.prompt,
            options=menu_info if len(menu_info) else None,
        )

    @classmethod
    def from_model_field(cls, model: BaseModel, field: str) -> Self:
        # TODO: add support for fields with choices
        return cls(
            name=field,
            prompt=model.model_fields[field].description,
        )

    def __str__(self):
        return f"<{self.name}: {[item.name for item in self.items.as_list]}>"


class MenuType(StrEnum):
    OPTIONS = auto()
    TEXT_INPUT = auto()
    MIXED = auto()


class MenuModel(BaseModel):
    name: str | None
    steps: list[MenuStep]

    @cached_property
    def menu_type(self) -> MenuType:
        types = {step.step_type for step in self.steps}
        if len(types) == 1:
            return types.pop()
        return MenuType.MIXED

    @cached_property
    def steps_number(self) -> int:
        return len(self.steps)

    @classmethod
    def from_menu_info(cls, *menu_infos: type[MenuInfo], name: str | None = None) -> Self:
        if len(menu_infos) == 1:
            name = name or menu_infos[0].name
            steps = [MenuStep.from_menu_info(menu_infos[0])]
            return cls(name=name, steps=steps)

        steps = [MenuStep.from_menu_info(m) for m in menu_infos]
        return cls(name=name, steps=steps)

    @classmethod
    def from_model(cls, model: BaseModel) -> Self:
        name = model.__class__.__name__
        fields = model.model_fields
        steps = [MenuStep(name=f_name, prompt=fields[f_name].description) for f_name in fields]
        return cls(name=name, steps=steps)

    def __str__(self):
        if self.steps_number == 1:
            return str(self.steps[0])
        return f"<{self.name or "Untitled menu"}: {self.steps_number} steps deep>"
