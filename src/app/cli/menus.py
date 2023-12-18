from abc import ABC, abstractmethod
from enum import StrEnum, auto
from functools import cached_property
from typing import Self

from app.cli.mods.models import MenuStep, MenuStepType
from app.cli.mods.representers import Representer
from app.cli.mods.manglers import InputMangler
from app.cli.mods.validators import Validator
from app.cli.utils import StepCounter


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


class Menu(ABC):
    """
    Abstract class for all menus.
    """
    __slots__ = ("_name", "_steps", "_representers", "_receivers", "_manglers", "_counter")

    def __init__(
        self,
        *steps: MenuStep,
        representer: Representer,
        validator: Validator,
        mangler: InputMangler,
        name: str | None = None,
    ):
        self._name = name
        self._steps = steps

        self._representer = representer
        self._validator = validator
        self._mangler = mangler

        self._validate_coherance()

        # self._counter = StepCounter(steps_number=self.steps_number)

    def _validate_coherance(self):

    @cached_property
    def menu_type(self) -> MenuType:
        return MenuType.from_step_types(*self._steps)

    @property
    def steps_number(self) -> int:
        return len(self._steps)

    @property
    def current_step_number(self) -> int:
        return self._counter.current_step

    def to_the_next_step(self) -> None:
        self._counter.increment()

    @abstractmethod
    def _validate_coherance(self) -> None:
        ...

    @abstractmethod
    def represent(self) -> str:
        ...

    @staticmethod
    def receive(*, input_request_text: str | None = None) -> str:
        return input(__prompt=input_request_text)

    @abstractmethod
    def validate(self, text_input: str) -> None:
        ...

    @abstractmethod
    def mangle(self, input_text: str) -> str:
        ...

    def __str__(self):
        if self.steps_number == 1:
            return str(self._steps[0])
        return f"<{self._name or "Untitled menu"}: {self.steps_number} steps deep>"


class HomogenicMenu(Menu):
    """
    Menu in which steps are processed the same way.
    """

    def __init__(
        self,
        *steps: MenuStep,
        representer: Representer,
        validator: Validator,
        mangler: InputMangler,
        name: str | None = None,
    ):
        super().__init__(
            *steps,
            representer=representer,
            validator=validator,
            mangler=mangler,
            name=name,
        )

    def _validate_coherance(self):
        if self.menu_type == MenuType.MIXED:
            raise ValueError("Menu model type must be HOMOGENIC.")

    def represent(self) -> str:
        menu_step = self._steps[self.current_step_number]
        return self._representer.represent(menu_step)

    def mangle(self, input_text: str) -> str:
        mangle_kwargs = {}
        if self.menu_type == MenuType.OPTIONS:
            option_name = self._steps[self.current_step_number].name
            mangle_kwargs["option_name"] = option_name
        elif self.menu_type == MenuType.TEXT_INPUT:
            field_name = self._steps[self.current_step_number].name
            mangle_kwargs["field_name"] = field_name
        return self._mangler.mangle(input_text, **mangle_kwargs)


class HeterogenicMenu(Menu):
    """
    Menu in which each step can be processed differently.
    """

    def __init__(
        self,
        *,
        steps: list[MenuStep],
        representers: list[MenuRepresenter],
        receivers: list[InputReceiver],
        manglers: list[InputMangler],
        name: str | None = None,
    ):
        super().__init__(
            steps=steps,
            representers=representers,
            receivers=receivers,
            manglers=manglers,
            name=name,
        )

    def _validate_coherance(self) -> None:
        if self.menu_type != MenuType.MIXED:
            raise ValueError("Menu model is homogenic, use HomogenicMenu.")

        mods = self._steps, self._representer, self._receiver, self._mangler
        if len({len(mod) for mod in mods}) != 1:
            raise ValueError(
                "The number of steps in the menu model and "
                "the number of menu components must be equal."
            )

    def represent(self) -> str:
        representer = self._representer[self.current_step_number]
        menu_step = self._steps[self.current_step_number]
        return representer.represent(menu_step)

    def mangle(self, input_text: str) -> str:
        mangler = self._mangler[self.current_step_number]
        menu_step = self._steps[self.current_step_number]
        return mangler.mangle(input_text)
