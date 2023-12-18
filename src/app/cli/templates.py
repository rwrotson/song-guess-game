from abc import ABC, abstractmethod
from functools import cache

from app.utils import classproperty, EnumeratedStrEnum, split_camel_case_string


class MenuTemplate(EnumeratedStrEnum, ABC):
    @classproperty
    @abstractmethod
    def prompt(self) -> str:
        pass

    @classmethod
    @classproperty
    @cache
    def name(cls) -> str:
        words = split_camel_case_string(cls.__name__)
        if words[-1] == "Menu" and len(words) > 1:
            words.pop()
        return " ".join(words)
