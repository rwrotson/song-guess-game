import re
import threading
from enum import StrEnum
from functools import cache
from typing import Callable, Self


def get_singleton_instance[T](cls: type["T"]) -> T:
    """
    Get existing instance of a singleton class or create a new one.
    """
    if not hasattr(cls, "_instance"):
        with threading.Lock():
            if not hasattr(cls, "_instance"):
                cls._instance = cls()
    return cls._instance


class _ClassPropertyDescriptor[T]:
    """
    Class property attribute (read-only).
    Same usage as @property, but taking the class as the first argument.
    """

    def __init__(self, func: Callable[[type[T]], T]) -> None:
        for attr in ("__doc__", "__module__", "__name__", "__qualname__"):
            if hasattr(func, attr):
                setattr(self, attr, getattr(func, attr))
        self.__wrapped__: Callable[[type[T]], T] = func

    def __set_name__(self, owner: type[T], name: str) -> None:
        self.__module__ = owner.__module__
        self.__name__ = name
        self.__qualname__ = owner.__qualname__ + "." + name

    def __get__(self, instance: T | None, owner: type[T] | None = None) -> type[T]:
        if owner is None:
            owner = type(instance)
        return self.__wrapped__(owner)


def classproperty(func: callable) -> _ClassPropertyDescriptor:
    """
    Class property attribute (read-only).
    """
    return _ClassPropertyDescriptor(func)


class EnumeratedStrEnum(StrEnum):
    @classmethod
    @classproperty
    @cache
    def as_list(cls) -> list[Self]:
        return [member for member in cls]

    @classmethod
    @classproperty
    @cache
    def length(cls) -> int:
        return len(cls.as_list)

    @classmethod
    @cache
    def get_enum_by_order_number(cls, order_number: int, /) -> Self:
        if 1 <= order_number <= cls.length:
            return list(cls)[order_number - 1]

        raise ValueError("Invalid order number")

    @classmethod
    @cache
    def get_name_by_order_number(cls, order_number: int, /) -> str:
        return cls.get_enum_by_order_number(order_number).name

    @classmethod
    @cache
    def get_order_number_by_name(cls, name: Self | str, /) -> int:
        if name in cls:
            return int(cls[name].value()) + 1
        raise ValueError("Invalid name")

    @property
    @cache
    def human_readable(self) -> str:
        return " ".join(split_snake_case_string(self.name))


def split_camel_case_string(string: str, /) -> list[str]:
    substring = re.sub("([A-Z]+)", r" \1", string)
    return re.sub("([A-Z][a-z]+)", r" \1", substring).split()


def split_snake_case_string(string: str, /) -> list[str]:
    return string.split("_")
