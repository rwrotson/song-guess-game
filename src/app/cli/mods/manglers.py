from enum import Enum
from typing import Protocol

from app.formatters import TemplateString


class InputMangler(Protocol):
    """
    Class that mangles user input.
    """

    @property
    def steps_number(self) -> int:
        ...

    def mangle(self, input_text: str, /, **kwargs) -> str:
        ...


class ManglingTemplate(Enum, TemplateString):
    DELETE = ""
    NO_MANGLING = "{input_text}"
    OPTIONS_MENU = "{bold}{name}{reset_style}: "
    SETTINGS_SECTION = "{bold}{name}{reset_style}: {input_text}"


def _mangle(text: str, /) -> str:
    _DELETE_LINE_CHAR = "\033[F"
    _CARRIAGE_RETURN_CHAR = "\r"

    def delete_n_lines_sequence(lines_number: int, /) -> str:
        return _DELETE_LINE_CHAR * lines_number

    return delete_n_lines_sequence(2) + text + _CARRIAGE_RETURN_CHAR


class OneStepMangler:
    def __init__(self, *, template: ManglingTemplate) -> None:
        self._template = template

    @property
    def steps_number(self) -> int:
        return 1

    def mangle(self, input_text: str, /, **kwargs) -> str:
        return _mangle(
            self._template.format(
                input_text,
                **kwargs,
            )
        )


class MultiStepMangler:
    def __init__(self, *templates: ManglingTemplate) -> None:
        self._templates = templates

    @property
    def steps_number(self) -> int:
        return len(self._templates)

    def mangle(self, input_text: str, /, *, step_number: int, **kwargs) -> str:
        return _mangle(
            self._templates[step_number].format(
                input_text,
                **kwargs,
            )
        )
