from functools import cache

from app.readme.texts import README_TEXTS
from app.utils import classproperty


class ReadmeModel:
    _texts = README_TEXTS

    @classmethod
    @classproperty
    def sections_number(cls) -> int:
        return len(cls._texts)

    @classmethod
    @cache
    def get_order_number_by_section_name(cls, section_name: str, /) -> int:
        if section_name in cls._texts:
            return list(cls._texts.keys()).index(section_name)

        raise ValueError("Invalid readme section name")

    @classmethod
    @cache
    def get_section_name_by_order_number(cls, order_number: int, /) -> str:
        if 0 <= order_number < cls.sections_number:
            return tuple(cls._texts.keys())[order_number]

        raise ValueError("Invalid order number")

    @classmethod
    @cache
    def get_text_by_order_number(cls, order_number: int, /) -> str:
        if 0 <= order_number < cls.sections_number:
            return tuple(cls._texts.values())[order_number]

        raise ValueError("Invalid order number")
