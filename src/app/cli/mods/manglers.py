from enum import StrEnum

from colorama import Style

from app.utils import classproperty


class ManglingTemplate(StrEnum):
    DELETE = ""
    NO_MANGLING = "{input_}"
    OPTIONS_MENU = "{bold}{option_name}{reset}: "
    SETTINGS_SECTION = "{bold}{field_name}{reset}: {input_}"

    @classproperty
    def formatting_styles(self) -> dict[str, str]:
        return {
            'bold': Style.BRIGHT,
            'reset': Style.RESET_ALL,
        }


class InputMangler:
    DELETE_LINE = "\033[F"
    CARRIAGE_RETURN = "\r"

    def __init__(self, *, template: ManglingTemplate) -> None:
        self._template = template

    def mangle(self, input_: str, /, **kwargs) -> str:
        mangled_input = self._template.format(
            input_=input_,
            **kwargs,
            **self._template.formatting_styles,
        )
        return self.delete_n_lines_sequence(2) + mangled_input + self.CARRIAGE_RETURN

    @classmethod
    def delete_n_lines_sequence(cls, lines_number: int, /) -> str:
        return cls.DELETE_LINE * lines_number
