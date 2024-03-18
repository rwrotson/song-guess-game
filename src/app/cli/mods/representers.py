from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import TYPE_CHECKING

from app.cli.formatters import TemplateString

if TYPE_CHECKING:
    from app.cli.models import MenuStep


class PromptTemplate(TemplateString, Enum):
    NO_PROMPT = ""
    ONLY_PROMPT = "${prompt}"
    BOLD_PROMPT = "${b}${prompt}${r}"
    PROMPT_WITH_NAME = "${clr_current}${b}${name}${r}: ${prompt}"


class DefaultTemplate(TemplateString, Enum):
    NO_DEFAULT = ""
    DEFAULT = "${b}(${r}default: ${b}${default})${r}"


class OptionsTemplate(TemplateString, Enum):
    NO_OPTIONS = ""
    WITH_NUMBER = "${number}. ${b}${option_name}${r}"
    WITH_NUMBER_AND_TAB = "\t${number}. ${b}${option_name}${r}"


@dataclass(slots=True, frozen=True)
class RepresenterTemplate:
    prompt_template: PromptTemplate
    options_template: OptionsTemplate
    default_template: DefaultTemplate = DefaultTemplate.NO_DEFAULT


class Representer:
    def __init__(self, *templates: RepresenterTemplate) -> None:
        self._representer_templates = templates

    @cached_property
    def steps_number(self) -> int:
        return len(self._representer_templates)

    def template(self, step_number: int) -> RepresenterTemplate:
        if self.steps_number == 1:
            return self._representer_templates[0]
        return self._representer_templates[step_number]

    def represent(
        self, step_model: "MenuStep", /, *, step_number: int = 0
    ) -> TemplateString:
        template = self.template(step_number=step_number)
        prompt_template, options_template, default_template = (
            template.prompt_template,
            template.options_template,
            template.default_template,
        )

        prompt = TemplateString("")
        if step_model.prompt is not None:
            prompt += prompt_template.safe_substitute(
                prompt=step_model.prompt,
                name=step_model.name,
            )
        if step_model.default is not None:
            prompt += " " + default_template.safe_substitute(
                default=step_model.default,
            )
        if step_model.options:
            if step_model.prompt is not None:
                prompt += "\n"
            prompt += "\n".join(
                [
                    str(
                        options_template.safe_substitute(
                            number=i + 1, option_name=option_name
                        )
                    )
                    for i, option_name in enumerate(step_model.options)
                ]
            )
            prompt += "\n"

        prompt += "\n"

        return prompt
