from enum import Enum
from functools import cached_property

from app.cli.formatters import TemplateString


class ManglingTemplate(TemplateString, Enum):
    DELETE = "\n\n"
    NO_MANGLING = "\n>>: ${clr_current}${b}${input_text}${r}\n\n"
    OPTIONS_MENU = "\n>>: ${clr_current}${b}${option_name}${r}\n\n"
    SETTINGS_SECTION = "\n>>${clr_current}${b}${option_name}${r}: ${input_text}\n\n"


class Mangler:
    __slots__ = ("_templates", "__dict__")

    def __init__(self, *templates: ManglingTemplate) -> None:
        self._templates = templates

    @cached_property
    def steps_number(self) -> int:
        return len(self._templates)

    def template(self, step_number: int) -> ManglingTemplate:
        if self.steps_number == 1:
            return self._templates[0]
        return self._templates[step_number]

    @staticmethod
    def _mangle(text: ManglingTemplate, /) -> TemplateString:
        _DELETE_LINE_CHAR = "\033[F"
        _CARRIAGE_RETURN_CHAR = "\r"

        def delete_n_lines_sequence(lines_number: int, /) -> str:
            return _DELETE_LINE_CHAR * lines_number

        text = delete_n_lines_sequence(2) + text + _CARRIAGE_RETURN_CHAR
        return TemplateString(text)

    def mangle(
        self,
        input_text: str,
        *,
        step_number: int = 0,
        option_name: str = "",
    ) -> TemplateString:
        mangled_text = self._mangle(
            self.template(step_number=step_number).safe_substitute(
                input_text=input_text, option_name=option_name
            )
        )
        return mangled_text
