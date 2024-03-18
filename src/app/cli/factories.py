from dataclasses import dataclass, field
from typing import Any, Callable, Self, Sequence

from pydantic import BaseModel

from app.cli.models import MenuStep, MenuType
from app.cli.mods import manglers, processors, representers, validators


type MenuOrigin = BaseModel | MenuStep | list[MenuStep]


@dataclass(slots=True, frozen=True)
class ParsedModel:
    """
    Class for parsing menu template into menu model blueprint.
    """
    name: str | None
    steps: Sequence[MenuStep]
    model: BaseModel | None = None

    @property
    def menu_type(self) -> MenuType:
        return MenuType.from_step_types(*self.steps)

    @classmethod
    def from_pydantic_model(cls, model: BaseModel, *, name: str | None = None) -> Self:
        name = name or model.__class__.__name__
        fields = model.model_fields
        steps = [MenuStep.from_model_field(model, f_name) for f_name in fields]
        return cls(name=name, steps=steps, model=model)

    @classmethod
    def from_any_origin(cls, menu_origin: MenuOrigin, /) -> Self:
        match menu_origin:
            case BaseModel():
                return cls.from_pydantic_model(menu_origin)
            case MenuStep():
                return cls(name=menu_origin.name, steps=[menu_origin])
            case list(MenuStep()):
                return cls(*menu_origin)
            case _:
                raise TypeError("Unsupported type for menu_origin")


@dataclass(slots=True, frozen=True)
class ParsedMods:
    representer: representers.Representer
    validator: validators.Validator
    mangler: manglers.Mangler
    processor: processors.Processor


type Mod = manglers.Mangler | processors.Processor | representers.Representer | validators.Validator


@dataclass(slots=True, frozen=True)
class ModOrigin[M: Mod]:
    model: type[M]
    params: dict[str, Any] = field(default_factory=dict)

    def construct_instance(self, **kwargs) -> M:
        return self.model(**self.params, **kwargs)


type ParsingMapping = Callable[[Any, ...], ModOrigin]
