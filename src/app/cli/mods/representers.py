from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from app.cli.mods.models import MenuStep
from app.formatters import TemplateString


class Representer(Protocol):
    def represent(self, step_model: MenuStep, /, **kwargs) -> str:
        ...

    @property
    def steps_number(self) -> int:
        ...


class PromptTemplate(Enum, TemplateString):
    NO_PROMPT = ""
    ONLY_PROMPT = "{prompt}"
    BOLD_PROMPT = "{bold}{prompt}{reset_style}"
    PROMPT_WITH_NAME = "{bold}{name}{reset_style}: {prompt}"


class OptionsTemplate(Enum, TemplateString):
    NO_OPTIONS = ""
    WITH_NUMBER = "{number}. {bold}{option_name}{reset_style}"
    WITH_NUMBER_AND_TAB = "\t{number}. {bold}{name}{reset_style}"


@dataclass(slots=True, frozen=True)
class RepresenterTemplate:
    prompt_template: PromptTemplate
    options_template: OptionsTemplate


def _represent(
    prompt_template: PromptTemplate,
    options_template: OptionsTemplate,
    menu_step: MenuStep,
) -> str:
    prompt = prompt_template.format(
        prompt=menu_step.prompt,
        name=menu_step.name,
    )
    options = [
        options_template.format(
            number=i + 1,
            name=option_name,
        )
        for i, option_name in enumerate(menu_step.options)
    ]
    options = "\n".join(options)

    return prompt + "\n" + options


class OneStepRepresenter:
    def __init__(self, representer_template: RepresenterTemplate) -> None:
        self._prompt_template = representer_template.prompt_template
        self._options_template = representer_template.options_template

    @property
    def steps_number(self) -> int:
        return 1

    def represent(self, menu_step: MenuStep) -> str:
        return _represent(
            prompt_template=self._prompt_template,
            options_template=self._options_template,
            menu_step=menu_step,
        )


class MultiStepRepresenter:
    def __init__(self, *representer_templates: RepresenterTemplate) -> None:
        self._representer_templates = representer_templates

    @property
    def steps_number(self) -> int:
        return len(self._representer_templates)

    def represent(self, step_model: MenuStep, *, step_number: int) -> str:
        representer_template = self._representer_templates[step_number]
        return _represent(
            prompt_template=representer_template.prompt_template,
            options_template=representer_template.options_template,
            menu_step=step_model,
        )
