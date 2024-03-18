import re
import threading
from enum import StrEnum
from functools import cache
from typing import (
    Callable,
    Protocol,
    runtime_checkable,
    Self,
    Generic,
    TypeVar,
)


def get_singleton_instance[T](cls: type["T"]) -> T | None:
    """
    Get existing instance of a singleton class or create a new one.
    """
    if not hasattr(cls, "_instance"):
        with threading.Lock():
            try:
                cls._instance = cls()
            except Exception as e:
                print(f"Failed to create instance of {cls.__name__}")
                print(e)
                return None
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


@runtime_checkable
class _Named(Protocol):
    name: str


Member = TypeVar("Member", bound=_Named)
Key = TypeVar("Key", bound=str)


class Registry(Generic[Key, Member]):
    # TODO: proposal to use this class in further refactorings
    def __init__(self, *members: Member, name: str) -> None:
        self.name = name

        if not members:
            self._members: dict[Key, Member] = {}
        else:
            self._members = {member.name: member for member in members}

    @property
    def members(self) -> dict[Key, Member]:
        return self._members

    @property
    def members_names(self) -> list[Key]:
        return list(self._members.keys())

    def add(self, *members: Member) -> None:
        for member in members:
            if not isinstance(member, _Named):
                raise TypeError(f"Member {member} does not have 'name' attribute")
            if member.name in self._members:
                raise ValueError(f"Member with name {member.name} already exists")

        for member in members:
            self._members[member.name] = member

    def find(self, name: Key, /) -> Member | None:
        return self._members.get(name, None)

    def get(self, name: Key, /) -> Member:
        if name not in self._members:
            raise ValueError(f"Member with name {name} does not exist")
        return self._members[name]

    def delete(self, name: Key, /) -> None:
        del self._members[name]

    # @classmethod
    # def from_regestries(cls, *registries: Self, name: str) -> Self:
    #     all_members = []
    #     all_members_names = []
    #     for registry in registries:
    #         for member in registry.members:
    #             if member.name in all_members_names:
    #                 raise ValueError(f"Member with name {member.name} already exists")
    #             all_members.append(member)
    #             all_members_names.append(member.name)
    #
    #     return cls(*all_members, name=name)

    def __contains__(self, name: Key, /) -> bool:
        return name in self._members

    def __iter__(self):
        return iter(self._members)

    def __len__(self) -> int:
        return len(self._members)


class Counter:
    """
    A class that keeps track of the current step number in the menu.
    """

    __slots__ = ("_min", "_max", "_current", "_start", "_step")

    def __init__(
        self, min_v: int, max_v: int, start_v: int | None = None, step: int = 1
    ) -> None:
        self._min = min_v
        self._max = max_v
        self._start = start_v or min_v
        self._current = start_v or min_v
        self._step = step

        self._validate()

    def _validate(self):
        if self._min > self._max:
            raise ValueError(
                f"Minimum value {self._min} is greater than maximum value {self._max}."
            )
        if self._current < self._min or self._current > self._max:
            raise ValueError(
                f"Start value {self._current} is not between {self._min} and {self._max}."
            )

    @property
    def current(self) -> int:
        return self._current

    @property
    def length(self) -> int:
        return self._max - self._min

    def increment(self) -> None:
        if self._current + self._step > self._max:
            raise StopIteration(f"Upper limit of counter == {self._max} exceeded.")
        self._current += self._step

    def decrement(self) -> None:
        if self._current - self._step < self._min:
            raise StopIteration(f"Lower limit of counter == {self._min} exceeded.")
        self._current -= self._step

    def reset(self) -> None:
        self._current = self._start

    def __len__(self):
        return self.length

    def __str__(self):
        return f"Counter(min={self._min}, max={self._max}, current={self._current})"


def timing_decorator(func):
    from time import time

    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:.5f} seconds to execute.")
        return result

    return wrapper
