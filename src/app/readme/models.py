from functools import cache

from app.cli.formatters import Text
from app.readme.texts import README_TEXTS


class TextsModel:
    def __init__(self, texts: dict[str, Text]) -> None:
        self._texts = texts

    @property
    def sections_number(self) -> int:
        return len(self._texts)

    @cache
    def get_order_number_by_section_name(self, text_title: str, /) -> int:
        if text_title in self._texts:
            return list(self._texts.keys()).index(text_title)
        raise ValueError("Invalid readme section name")

    @cache
    def get_section_name_by_order_number(self, order_number: int, /) -> Text:
        if 0 <= order_number < self.sections_number:
            return tuple(self._texts.keys())[order_number]
        raise ValueError("Invalid order number")

    @cache
    def get_text_by_order_number(self, order_number: int, /) -> Text:
        if 0 <= order_number < self.sections_number:
            return tuple(self._texts.values())[order_number] + "\n"
        raise ValueError("Invalid order number")


README_MODEL = TextsModel(README_TEXTS)
