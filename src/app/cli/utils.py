from dataclasses import dataclass
from random import randrange
from time import sleep

from app.cli.formatters import FORMATTERS


RESET_SYMBOL = "\033[0m"  # TODO: add support for various resets


@dataclass(frozen=True, slots=True)
class _PreparedText:
    text: str
    format_sequences: dict[int, list[str]]  # k: index_of_start, v: format_sequences
    reset_sequences: dict[int, list[str]]


def _prepare_string(text: str) -> _PreparedText:
    reset_sequences = [RESET_SYMBOL]
    format_sequences = [v for v in FORMATTERS.values() if v not in reset_sequences]

    i = 0
    prepared_text = ""
    prepared_text_length = 0
    opening_symbols, closing_symbols = {}, {}

    while i < len(text):
        opening_symbol, closing_symbol = None, None
        if text[i : i + 4] in format_sequences:
            opening_symbol = text[i : i + 4]
            i += 4
        elif text[i : i + 5] in format_sequences:
            opening_symbol = text[i : i + 5]
            i += 5

        elif text[i : i + 4] in reset_sequences:
            closing_symbol = text[i : i + 4]
            i += 4
        elif text[i : i + 5] in reset_sequences:
            closing_symbol = text[i : i + 5]
            i += 5
        else:
            prepared_text += text[i]
            i += 1

        if opening_symbol:
            if opening_symbols.get(prepared_text_length) is None:
                opening_symbols[prepared_text_length] = []
            opening_symbols[prepared_text_length].append(opening_symbol)
        if closing_symbol:
            if closing_symbols.get(prepared_text_length) is None:
                closing_symbols[prepared_text_length] = []
            closing_symbols[prepared_text_length] = closing_symbol

        if not opening_symbol and not closing_symbol:
            prepared_text_length += 1

    return _PreparedText(
        text=prepared_text,
        format_sequences=opening_symbols,
        reset_sequences=closing_symbols,
    )


def _get_random_time_in_s(min_delay: int, max_delay: int) -> float:
    if min_delay == max_delay:
        return min_delay / 1000
    return randrange(min_delay, max_delay) / 1000


def imitate_typing(text: str, *, min_delay: float, max_delay: float) -> None:
    min_delay = int(min_delay * 1000) or 1
    max_delay = int(max_delay * 1000) or 1

    prepared_text = _prepare_string(text)

    active_modifiers = []
    for i in range(len(prepared_text.text)):
        delay = _get_random_time_in_s(min_delay, max_delay)
        sleep(delay)

        if modifiers := prepared_text.format_sequences.get(i):
            active_modifiers.extend(modifiers)

        modifier = prepared_text.reset_sequences.get(i)
        if modifier == RESET_SYMBOL:
            active_modifiers = []

        char_to_print = prepared_text.text[i]

        is_formatted: bool = False
        for modifier in active_modifiers:
            char_to_print = modifier + char_to_print
            is_formatted = True
        if is_formatted:
            char_to_print += RESET_SYMBOL

        print(char_to_print, end="", flush=True)
