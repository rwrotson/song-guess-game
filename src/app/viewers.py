from typing import Self

from app.cli.colors import Color
from app.cli.formatters import Text
from app.cli.viewers import TypingDisabledViewer, TypingEnabledViewer, Viewer
from app.game.models import get_game
from app.settings.models import get_settings
from app.utils import get_singleton_instance


class ColorTheme:
    __slots__ = ("_default", "_players")

    def __init__(self):
        players_number = len(get_game().players)

        if is_color_enabled := get_settings().display.color_enabled:
            self._default = Color.get_next_color()
            self._players = [Color.get_next_color() for _ in range(players_number)]
        else:
            self._default = Color.TW
            self._players = [Color.TW for _ in range(players_number)]

    @property
    def default(self):
        return self._default

    @property
    def players(self):
        return self._players

    def refreshed(self):
        self.__init__()
        return self

    def to_dict(self) -> dict[str, Color]:
        d = {f"clr_{i + 1}": color.value for i, color in enumerate(self.players)}
        d |= {"clr_0": self.default.value}
        return d

    def __getitem__(self, index: int) -> Color:
        try:
            return self.players[index + 1]
        except IndexError:
            pass
        return self.default


def get_color_theme() -> ColorTheme:
    return get_singleton_instance(cls=ColorTheme)


def _viewer_factory() -> Viewer:
    settings = get_settings()
    display_settings = settings.display if settings else None
    color_theme_dict = get_color_theme().to_dict()

    typing_mapping = {
        True: {
            "class": TypingEnabledViewer,
            "params": {
                "formatters_dict": color_theme_dict,
                "max_delay": display_settings.max_delay,
                "min_delay": display_settings.min_delay,
            },
        },
        False: {
            "class": TypingDisabledViewer,
            "params": {
                "formatters_dict": color_theme_dict,
            },
        },
        None: {
            "class": TypingDisabledViewer,
            "params": {
                "formatters_dict": color_theme_dict,
            },
        },
    }

    is_typing_enabled = display_settings.typing_enabled
    viewer_class = typing_mapping[is_typing_enabled]["class"]
    viewer_params = typing_mapping[is_typing_enabled]["params"]

    return viewer_class(**viewer_params)


class AppViewer:
    """
    Class that contains all viewers used in the app.
    """

    __slots__ = ("_color_theme", "_viewer", "_simple_viewer")

    def __init__(self):
        self._color_theme: ColorTheme = get_color_theme().refreshed()
        self._viewer: Viewer = _viewer_factory()
        self._simple_viewer = TypingDisabledViewer(
            formatters_dict=self._color_theme.to_dict(),
        )

    def refreshed(self) -> Self:
        self.__init__()
        return self

    @property
    def color_theme(self):
        return self._color_theme

    def get_current_color(self) -> Color:
        if get_game().status != "in_progress":
            return self._color_theme.default
        player_id = get_game().counter.current_player_id

        return self._color_theme.players[player_id]

    def display(self, text: Text, *, formatters_dict: dict[str, str] = None) -> None:
        formatters_dict = formatters_dict or {}
        formatters_dict |= {"clr_current": self.get_current_color().value}

        self._viewer.display(text, formatters_dict=formatters_dict)

    def print(self, text: Text, *, formatters_dict: dict[str, str] = None) -> None:
        formatters_dict = formatters_dict or {}
        formatters_dict |= {"clr_current": self.get_current_color().value}

        self._simple_viewer.display(text, formatters_dict=formatters_dict)
