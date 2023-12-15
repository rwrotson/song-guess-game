from app.abstract.viewers import Viewer
from app.formatters import bold, separate_line, colored_fore, imitate_typing, ForeColor
from app.settings.models import DisplaySettings


def _format_text(text: str, /, is_bold: bool = False, is_sep_line: bool = True) -> str:
    if is_bold:
        text = bold(text)
    if is_sep_line:
        text = separate_line(text)
    return text


class TypingDisabledViewer:
    __slots__ = ("color",)

    def __init__(self, color: ForeColor = ForeColor.WHITE) -> None:
        self.color = color

    def display(self, text: str, /, is_bold: bool = False, is_sep_line: bool = True) -> None:
        text = _format_text(text, is_bold=is_bold, is_sep_line=is_sep_line)
        print(
            colored_fore(text, color=self.color),
            end="",
            flush=True,
        )


class TypingEnabledViewer:
    __slots__ = ("min_delay", "max_delay", "color")

    def __init__(self, min_delay: float, max_delay: float, color: ForeColor = ForeColor.WHITE) -> None:
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.color = color

    def display(self, text: str, is_bold: bool = False, is_sep_line: bool = True) -> None:
        text = _format_text(text, is_bold=is_bold, is_sep_line=is_sep_line)
        imitate_typing(
            colored_fore(text, color=self.color),
            min_delay=self.min_delay,
            max_delay=self.max_delay,
        )


def viewer_factory(display_settings: DisplaySettings, *, color: ForeColor.WHITE) -> Viewer:
    is_typing_enabled = display_settings.typing_enabled

    typing_mapping = {
        is_typing_enabled: {
            "class": TypingEnabledViewer,
            "params": {
                "color": color,
                "max_delay": display_settings.max_delay,
                "min_delay": display_settings.min_delay,
            },
        },
        not is_typing_enabled: {
            "class": TypingDisabledViewer,
            "params": {
                "color": color,
            },
        },
    }

    viewer_class = typing_mapping[is_typing_enabled]["class"]
    viewer_params = typing_mapping[is_typing_enabled]["params"]

    return viewer_class(**viewer_params)


class ViewersContainer:
    """
    Class that contains all viewers used in the app.
    """
    _colors: list[ForeColor]
    _default_viewer: Viewer
    _players_viewers: list[Viewer]

    def __init__(self, players_number: int, display_settings: DisplaySettings) -> None:
        self.update_colors(players_number=players_number, display_settings=display_settings)
        self.update_viewers(display_settings=display_settings)

    def update_colors(self, players_number: int, display_settings: DisplaySettings) -> None:
        if display_settings.color_enabled:
            self._colors = [ForeColor.get_next_color() for _ in range(players_number)]
        else:
            self._colors = [ForeColor.WHITE for _ in range(players_number)]

    def update_viewers(self, display_settings: DisplaySettings) -> None:
        self._default_viewer = viewer_factory(display_settings, color=ForeColor.WHITE)
        self._players_viewers = [viewer_factory(display_settings, color=c) for c in self._colors]

    @property
    def default_viewer(self) -> Viewer:
        return self._default_viewer

    @property
    def colors(self) -> list[ForeColor]:
        return self._colors

    def players_viewer(self, player_number: int, /) -> Viewer:
        return self._players_viewers[player_number]

    def players_color(self, player_number: int, /) -> ForeColor:
        return self._colors[player_number]
