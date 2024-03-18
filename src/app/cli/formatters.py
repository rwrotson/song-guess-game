from enum import StrEnum
from typing import override, Self
from string import Template

from app.cli.colors import COLOR_FORMATTERS


class Style(StrEnum):
    B = "\033[1m"  # bold
    D = "\033[2m"  # dim
    I = "\033[3m"  # italic
    U = "\033[4m"  # underline
    RB = "\033[21m"  # reset_bold
    RD = "\033[22m"  # reset_dim
    RI = "\033[23m"  # reset_italic
    RU = "\033[24m"  # reset_underline
    R = "\033[0m"  # reset_all

    def wrap_text(self, text):
        return self.value + text + Style.R.value


STYLE_FORMATTERS = {k.lower(): v for k, v in Style.__members__.items()}


FORMATTERS = {**STYLE_FORMATTERS, **COLOR_FORMATTERS}


class TemplateString(Template):
    @staticmethod
    def _patch_custom_formatters(kwargs: dict) -> dict:
        for k, v in kwargs.items():
            if v is None:
                kwargs[k] = ""
        kwargs.update(FORMATTERS)
        return kwargs

    @override
    def substitute(self, /, **kwargs) -> str:
        kwargs = self._patch_custom_formatters(kwargs)
        return super().substitute(kwargs)

    @override
    def safe_substitute(self, /, **kwargs) -> Self:
        kwargs = self._patch_custom_formatters(kwargs)
        return super().safe_substitute(kwargs)

    def __add__(self, other: str | Self):
        self.template += str(other)
        return self

    def __radd__(self, other: str | Self):
        self.template = str(other) + self.template
        return self

    def __iadd__(self, other: str | Self):
        self.template += str(other)
        return self


type Text = str | TemplateString


def bold(text: str, /) -> str:
    return Style.B + text + Style.R
