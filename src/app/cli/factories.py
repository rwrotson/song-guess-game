from dataclasses import dataclass
from functools import cached_property
from typing import Any, ClassVar, Self

from pydantic import BaseModel

from app.cli.exceptions import WrongMenuTypeError
from app.cli.menus import Menu, HomogenicMenu, HeterogenicMenu, MenuType
from app.cli.mods.manglers import InputMangler, ManglingTemplate
from app.cli.mods.models import MenuStepType, MenuStep
from app.cli.mods.representers import Representer
from app.cli.mods.validators import Validator
from app.cli.templates import MenuTemplate


_MenuOrigin = BaseModel | type[MenuTemplate] | list[type[MenuTemplate]]


@dataclass(slots=True, frozen=True)
class _ParsedModel:
    """
    Class for parsing menu template into menu model blueprint.
    """
    name: str | None
    steps: list[MenuStep]
    model: BaseModel | None = None

    @cached_property
    def menu_type(self) -> MenuType:
        return MenuType.from_step_types(*self.steps)

    @classmethod
    def from_menu_infos(cls, *menu_infos: type[MenuTemplate], name: str | None = None) -> Self:
        steps = [MenuStep.from_menu_info(menu_info) for menu_info in menu_infos]
        return cls(name=name, steps=steps)

    @classmethod
    def from_pydantic_model(cls, model: BaseModel, *, name: str | None = None) -> Self:
        name = name or model.__class__.__name__
        fields = model.model_fields
        steps = [MenuStep.from_model_field(model, f_name) for f_name in fields]
        return cls(name=name, steps=steps, model=model)

    @classmethod
    def from_any_origin(cls, menu_origin: _MenuOrigin) -> Self:
        match menu_origin:
            case BaseModel():
                return _ParsedModel.from_pydantic_model(menu_origin)
            case type(MenuTemplate()):
                return _ParsedModel.from_menu_infos(menu_origin)
            case list(type(MenuTemplate())):
                return _ParsedModel.from_menu_infos(*menu_origin)
            case _:
                raise TypeError("Unsupported type for menu_origin")


@dataclass(slots=True, frozen=True)
class _ParsedStepMods:
    """
    Class for parsing menu step type into step modifiers.
    """

    representer: Representer
    validator: Validator
    mangler: InputMangler

    MAPPING: ClassVar[dict[MenuStepType, dict[str, Any]]] = {
        MenuStepType.OPTIONS: {
            "representer": {
                "prompt_template": "",
                "options_template": "",
            },
            "mangling_template": ManglingTemplate.OPTIONS_MENU,
            "validator": "",
        },
        MenuStepType.TEXT_INPUT: {
            "representer": TextInputRepresenter,
            "mangling_template": ManglingTemplate.SETTINGS_SECTION,
        },
    }

    @classmethod
    def from_step_type(cls, step_type: MenuStepType, /) -> Self:
        return cls(
            representer=cls.MAPPING[step_type]["representer"],
            validator=,
            mangler=InputMangler(
                template=cls.MAPPING[step_type]["mangling_template"],
            ),
        )

    @classmethod
    def from_menu_step(cls, menu_step: MenuStep, /) -> Self:
        return cls.from_step_type(menu_step.step_type)


def homogenic_menu_factory(menu_origin: _MenuOrigin, /, *, parsed_model: _ParsedModel = None) -> HomogenicMenu:
    if not parsed_model:
        parsed_model = _ParsedModel.from_any_origin(menu_origin)

    if parsed_model.menu_type == MenuType.MIXED:
        raise WrongMenuTypeError("Menu model type must be HOMOGENIC.")

    parsed_mods = _ParsedStepMods.from_menu_step(parsed_model.steps[0])

    return HomogenicMenu(
        name=parsed_model.name,
        steps=parsed_model.steps,
        representers=parsed_mods.representer,
        receivers=parsed_mods.receiver,
        manglers=parsed_mods.mangler,
    )


def heterogenic_menu_factory(menu_origin: _MenuOrigin, /, *, parsed_model: _ParsedModel = None) -> HeterogenicMenu:
    if not parsed_model:
        parsed_model = _ParsedModel.from_any_origin(menu_origin)

    if parsed_model.menu_type != MenuType.MIXED:
        raise WrongMenuTypeError("Menu model type must be HETEROGENIC.")

    mods = [_ParsedStepMods.from_menu_step(step) for step in parsed_model.steps]
    representers, receivers, manglers = zip(*mods)

    return HeterogenicMenu(
        name=parsed_model.name,
        steps=parsed_model.steps,
        representers=representers,
        receivers=receivers,
        manglers=manglers,
    )


def menu_factory(menu_origin: _MenuOrigin, /) -> Menu:
    parsed_model = _ParsedModel.from_any_origin(menu_origin)

    if parsed_model.menu_type == MenuType.MIXED:
        return heterogenic_menu_factory(menu_origin, parsed_model=parsed_model)

    return homogenic_menu_factory(menu_origin, parsed_model=parsed_model)
