from app.utils import EnumeratedStrEnum, get_singleton_instance


class Color(EnumeratedStrEnum):
    R = "\033[31m"  # red
    G = "\033[32m"  # green
    Y = "\033[33m"  # yellow
    B = "\033[34m"  # blue
    M = "\033[35m"  # magenta
    C = "\033[36m"  # cyan
    LR = "\033[91m"  # light_red
    LG = "\033[92m"  # light_green
    LY = "\033[93m"  # light_yellow
    LB = "\033[94m"  # light_blue
    LM = "\033[95m"  # light_magenta
    LC = "\033[96m"  # light_cyan

    W = "\033[97m"  # white
    TW = "\033[39m"  # true_white / default

    RESET = "\033[0m"  # reset_all

    @staticmethod
    def get_next_color():
        generator = _get_color_generator()
        return next(generator)

    def wrap_text(self, text: str) -> str:
        if self == Color.TW:
            return text
        return self.value + text + self.RESET.value


COLOR_FORMATTERS = {f"clr_{k.lower()}": v for k, v in Color.__members__.items()}


class _ColorGenerator:
    def __init__(self) -> None:
        from random import randint

        self.max_color_number = len(Color) - 3  # exclude two whites and reset
        self._current_color_number = randint(1, self.max_color_number)

    def __next__(self) -> Color:
        if self._current_color_number > self.max_color_number:
            self._current_color_number = 1

        color = Color.get_enum_by_order_number(self._current_color_number)
        self._current_color_number += 1

        return color


def _get_color_generator() -> _ColorGenerator:
    return get_singleton_instance(cls=_ColorGenerator)
