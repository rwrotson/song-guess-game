from typing import Literal

from pydantic import ValidationError

from app.cli.formatters import TemplateString
from app.cli.mods.processors import Input
from app.game.models import Player
from app.state import Stage, get_state


class MainMenuProcessor:
    def process(self, input_: Input, step_number: int = 0) -> None:
        assert isinstance(input_.validated, int), "Invalid input."

        state = get_state()

        match input_.option_name:
            case "PLAY":
                state.restart_game()
            case "RESUME":
                state.resume_game()
            case "SETTINGS":
                state.stage = Stage.SETTINGS.value.ALL_SETTINGS
            case "README":
                state.stage = Stage.README
            case "LIBRARIES_STATS":
                state.stage = Stage.LIBRARIES_STATS
            case "EXIT":
                state.exit_game()
            case _:
                raise ValueError("Invalid input.")


class LibrariesStatsProcessor:
    @staticmethod
    def _display_stats(
        players: list[Player], repr_type: Literal["short", "extended"]
    ) -> None:
        state = get_state()
        if not players:
            state.viewer.display("No player libraries set up.")
            return

        mapping = {
            "short": "get_library_short_repr",
            "extended": "get_library_extended_repr",
        }

        for i, player in enumerate(players):
            stats_repr = getattr(player, mapping[repr_type])()
            state.viewer.display(TemplateString(f"$clr_{i + 1}{stats_repr}\n"))

    def process(self, input_: Input, step_number: int = 0) -> None:
        assert isinstance(input_.validated, int), "Invalid input."

        state = get_state()
        players = state.game.players

        match input_.option_name:
            case "PREVIOUS_SHORT_STATS" | "SHORT_STATS":
                self._display_stats(players=players, repr_type="short")
            case "PREVIOUS_EXTENDED_STATS" | "EXTENDED_STATS":
                self._display_stats(players=players, repr_type="extended")
            case "NEXT_SHORT_STATS":
                self._display_stats(players=players, repr_type="short")
            case "NEXT_EXTENDED_STATS":
                self._display_stats(players=players, repr_type="extended")
            case "BACK":
                state.stage = Stage.MAIN_MENU
            case _:
                raise ValueError("Invalid input.")


class SettingsProcessor:
    def process(self, input_: Input, step_number: int = 0) -> None:
        assert isinstance(input_.validated, int), "Invalid input."

        state = get_state()

        match (input_.validated, input_.option_name):
            case (1, "MAIN_SETTINGS"):
                state.stage = Stage.SETTINGS.value.MAIN_SETTINGS
            case (2, "ADVANCED_SETTINGS"):
                state.stage = Stage.SETTINGS.value.ADVANCED_SETTINGS
            case (3, "SHOW_CURRENT_SETTINGS"):
                text = state.settings.config_file_as_str()
                state.viewer.display(text)
            case (4, "EDIT_CONFIG_FILE"):
                try:
                    state.settings.edit_config_file()
                except ValidationError as e:
                    state.viewer.display(str(e))
                    state.stage = Stage.SETTINGS.value.ALL_SETTINGS
            case (5, "SET_DEFAULT_SETTINGS"):
                state.settings.set_to_default()
                state.viewer.display("Settings have been set to default.")
            case (6, "BACK"):
                state.stage = Stage.MAIN_MENU
            case _:
                raise ValueError("Invalid input.")


class MainSettingsProcessor:
    def process(self, input_: Input, step_number: int = 0) -> None:
        assert isinstance(input_.validated, int), "Invalid input."

        state = get_state()

        match (input_.validated, input_.option_name):
            case (1, "GAME"):
                state.stage = Stage.MAIN_SETTINGS.value.GAME
            case (2, "PLAYERS"):
                state.stage = Stage.SETTINGS.value.PLAYERS
            case (3, "BACK"):
                state.stage = Stage.SETTINGS.value.ALL_SETTINGS
            case _:
                raise ValueError("Invalid input.")


class AdvancedSettingsProcessor:
    def process(self, input_: Input, step_number: int = 0) -> None:
        assert isinstance(input_.validated, int), "Invalid input."

        state = get_state()

        match (input_.validated, input_.option_name):
            case (1, "DISPLAY"):
                state.stage = Stage.ADVANCED_SETTINGS.value.DISPLAY
            case (2, "SELECTION"):
                state.stage = Stage.ADVANCED_SETTINGS.value.SELECTION
            case (3, "SAMPLING"):
                state.stage = Stage.ADVANCED_SETTINGS.value.SAMPLING
            case (4, "PLAYBACK_BAR"):
                state.stage = Stage.ADVANCED_SETTINGS.value.PLAYBACK_BAR
            case (5, "EVALUATION"):
                state.stage = Stage.ADVANCED_SETTINGS.value.EVALUATION
            case (6, "SERVICE_PATHS"):
                state.stage = Stage.ADVANCED_SETTINGS.value.SERVICE_PATHS
            case (7, "BACK"):
                state.stage = Stage.SETTINGS.value.ALL_SETTINGS
            case _:
                raise ValueError("Invalid input.")


class PlayersSettingsProcessor:
    def process(self, input_: Input, step_number: int = 0) -> None:
        assert isinstance(input_.validated, int), "Invalid input."

        state = get_state()

        current_players_number = state.settings.game.players_number

        if input_.validated in range(1, current_players_number + 1):  # player N
            state.stage = Stage.MAIN_SETTINGS.value.PLAYER
            state.data["player_number"] = input_.validated  # counting from 1

        elif input_.validated == current_players_number + 1:  # back
            state.stage = Stage.SETTINGS.value.MAIN_SETTINGS

        else:
            raise ValueError("Invalid input.")
