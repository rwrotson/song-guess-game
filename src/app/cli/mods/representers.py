from typing import Protocol

from app.cli.core.models import MenuStep
from app.formatters import bold


class MenuRepresenter(Protocol):
    @staticmethod
    def represent(step_model: MenuStep) -> str:
        ...


class OptionsRepresenter:
    @staticmethod
    def represent(step_model: MenuStep) -> str:
        text_to_display = f"{bold(step_model.name)}: {step_model.prompt}\n"
        for i, option in enumerate(step_model.options):
            text_to_display += f"\t{i + 1}. {bold(option)}\n"
        return text_to_display


class TextInputRepresenter:
    @staticmethod
    def represent(step_model: MenuStep) -> str:
        return f"{bold(step_model.prompt)}\n"

